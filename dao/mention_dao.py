# coding=utf8

from base import BaseQuery

class MentionsDao(BaseQuery):
    tb_name= 'mentions'

class MentionUsersDao(BaseQuery):
    tb_name = 'mention_users'

Mention = BaseQuery('mentions')

MentionUser = BaseQuery('mention_users')