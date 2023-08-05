"""
@Description: 
@Usage: 
@Author: liuxianglong
@Date: 2022/9/20 下午2:11
"""


class SelfResponse(object):

    def __init__(self):
        self.code = 200
        self.data = ''
        self.message = 'ok'

    def to_dict(self):
        pass
