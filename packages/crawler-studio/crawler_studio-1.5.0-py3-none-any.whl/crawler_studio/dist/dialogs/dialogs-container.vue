<template>
  <div class="dialog-root">
    <template v-for="(dialog) in dialogs">
      <dialog-item :options="dialog" :key="dialog.instance.id"></dialog-item>
    </template>
  </div>
</template>

<script>
import {DialogItem} from '../adapter'
import {LoggerService} from "../logger/logger.service";
import {DialogService} from "./dialog.service";
import {State} from "./dialog";
import {EscapeContext, getContext} from "../base/event-context";

export default {
  name: "dialogs-container",
  components: {
    [DialogItem.name]: DialogItem
  },
  data() {
    return {
      dialogs: [],
      subs: []
    }
  },
  di: {
    inject: {
      ls: LoggerService,
      ds: DialogService
    }
  },
  watch: {
    dialogs() {
      this.refreshHiddenStatus()
    }
  },
  created() {
    const context = getContext(EscapeContext)
    this.subs.push(
        this.ds.dialog.subscribe(d => {
          this.dialogs.push(d)
          d.instance.afterClosed().finally(() => {
            this.dialogs.splice(this.dialogs.indexOf(d), 1)
          }).catch(err => {})
        }),
        context.events.subscribe(e => {
          if(this.dialogs.length) {
            const lastOne = this.dialogs[this.dialogs.length - 1]
            if(lastOne.instance._vm?.enableEscClose) {
              lastOne.instance.close()
            }
          }
        })
    )
  },
  mounted() {

  },
  destroyed() {
    if (this.subs && this.subs.length) {
      this.subs.forEach(item => item.unsubscribe())
      this.subs = []
    }
  },
  methods: {
    refreshHiddenStatus() {
      this.dialogs.filter(c => {
        if(!c.instance.config) {
          return true
        }
        if(c.instance.config.backgroundCover !== undefined) {
          return !!c.instance.config.backgroundCover
        }
        if(c.instance.config.anchor) {
          return false
        }
        return true
      }).forEach((item, index, arr) => {
        if(item.instance._state._value === State.opened) {
          item.instance._vm.hide = index !== arr.length - 1
        } else {
          item.instance.afterOpened().then(() => {
            item.instance._vm.hide = index !== arr.length - 1
          })
        }
      })
    }
  }
}
</script>
<style lang="less" scoped>
.dialog-root {
  //> :not(:last-child) {
  //  opacity: 0;
  //}
}
</style>
