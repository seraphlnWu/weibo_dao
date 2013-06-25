# coding=utf8

from base import BaseQuery

class RepostsDao(BaseQuery):
    tb_name = 'reposts'

Repost = RepostsDao('reposts')
