# coding=utf8

from weibo_dao.dao.utils import get_crm_db
from weibo_dao.dao.utils import DB_PLATFORM_MAPPER


def get_distinct_data(collection_name, field, db=None):
    '''
        get the distinct result
        input:
            @collection_name -> the target collection
            @field -> the distinct field
            @db -> the given db instancs
        output:
            @_ -> the distinct result
    '''
    db = db or get_crm_db()
    return db[collection_name].distinct(field)


def get_platform_accounts(platform, db=None):
    '''
        get accounts by given platform
        input:
            @platform -> the target platform
            @db -> the given db instancs
        output:
            @_ -> accounts list or an empty list
    '''
    return list(db.crm_accounts.find({
        'platform': platform,
        'is_del': {'$ne': True}},
    ))


def get_api_since_id(uid, platform, field, db=None):
    '''
        get given uesr's since_id for get data from given platform data source

        input:
            @uid -> the target user
            @platform -> data source platform (sina, tencent, etc...)
            @field -> because there are several kinds of since_id, so I need
                to know the specific field
            @db -> the given db instance
        output:
            @since_id -> the given field, given platform, given user's sinceid
    '''
    w_db = db or DB_PLATFORM_MAPPER[platform]()
    user = w_db.users.find_one({'_id': uid}, {field: 1}) or {}
    return user.get(field) or 0


def update_user_since_id(uid, platform, field, value, db=None):
    '''
        update the given user's since_id

        input:
            @uid -> the target user id
            @platform -> the target platform
            @field -> the to be updated column
            @value -> the value to be updated column
            @db -> the given db instance
        output:
            @_ -> the update result
    '''
    w_db = db or DB_PLATFORM_MAPPER[platform]()
    return w_db.users.update({'_id': uid}, {'$set': {field: value}}, safe=True)


def save_data_by_platform(platform, collection, data, db=None):
    '''
        save data to given platform and given data index

        input:
            @platform -> the given platform to store data
            @collection -> the given collection to store data
            @data -> the to be stored document
            @db -> the db instance
        output:
            @_ -> the result of this operation
    '''
    w_db = db or DB_PLATFORM_MAPPER[platform]()
    return w_db[collection].save(data)
