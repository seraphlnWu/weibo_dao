# coding=utf8
from utils import MONGODB_INSTANCE as db

from influence_dao import get_cur_influence

from statistic_dao import get_followers_quality_distr
from statistic_dao import get_followers_tags_distr
from statistic_dao import get_followers_location_distr
from statistic_dao import get_followers_gender_distr
from statistic_dao import get_followers_activeness_distr


def get_users():
    ''' 获取全部的有效用户信息列表 '''
    return db.users.find({'sm_deleted': {'$ne': True}})


def get_whole_users():
    ''' 获取全部用户的信息列表 '''
    return db.users.find()


def get_user_by_id(uid):
    ''' 根据传入的uid获取相应的user信息 '''
    return db.users.find_one({'_id': uid})


def get_user_by_keyword(uid, *keywords):
    ''' 根据传入的uid列表获取相应的user信息 '''
    query_dict = dict([(cur_key, 1) for cur_key in keywords])
    return db.users.find_one({'_id': uid}, query_dict)


def get_user_info(uid, default=['id', 'screen_name']):
    ''' 获取用户基本信息 '''
    query_dict = {'id': 1, 'screen_name': 1}
    return db.users.find_one({'_id': uid}, query_dict)


def get_tasks(uid):
    ''' get a task list by uid '''
    tmp_user = db.users.find_one({'_id': uid}) or {}
    return tmp_user.get('tasks', []) 


def get_user(uid):
    '''
        获取用户基本信息，
        若库中没有用户记录，则按照
        new_user参数初始化用户基本信息。
    '''
    resultdict = db.users.find_one({'_id': uid})

    if not resultdict:
        return {}

    influence = get_cur_influence(uid)
    resultdict['friends_count'] = influence.get('friends_count', 0)
    resultdict['followers_count'] = influence.get('followers_count', 0)
    resultdict['statuses_count'] = influence.get('statuses_count', 0)
    resultdict['influence'] = influence.get('influence', 0)
    resultdict['fans_quality'] = resultdict['influence']/resultdict['followers_count'] if resultdict['followers_count'] else 0
    resultdict['account_activeness'] = influence.get('account_activeness', 0)
    resultdict['followers_activeness'] = influence.get('followers_activeness', 0)

    resultdict['followers_quality_dist'] = get_followers_quality_distr(uid)
    resultdict['followers_location_dist'] = get_followers_location_distr(uid)
    resultdict['followers_genders_dist'] = get_followers_gender_distr(uid)
    resultdict['followers_activeness_dist'] = get_followers_activeness_distr(uid)
    resultdict['followers_tags_dist'] = get_followers_tags_distr(uid)

    if resultdict.get('url', '').strip() == 'http://1':
        resultdict['url'] = ''

    return resultdict


def get_fuids(uid, with_followbrand_count=False):
    ''' get followbrand list '''
    info = get_user_by_keyword(uid, *{'fuids': 1, 'max_followbrand_count': 1})
    if with_followbrand_count:
        return (info.get('fuids', []), info.get('max_followbrand_count', None))
    else:
        return info.get('fuids', [])


def add_task(uid, task):
    ''' 添加一个新的待发送的微博 '''
    task_list = get_tasks(uid)
    task_list.append(task)
    task_list.sort(key=lambda x:x.get('eta'))

    task_length = len(task_list)
    cur_index = task_list.index(task)
    k = cur_index + 1  # if cur_index < len(task_list)-1 else cur_index
    j = cur_index - 1  # if cur_index > 0 else 0

    if any([
        (j >= 0) and (task['message'] == task_list[j].get("message")),
        k < task_length and (task['message'] == task_list[k]["message"]),
        (j >= 0 and (task['eta'] - task_list[j].get('eta')) < 60),
        (k < task_length and (task['eta'] - task_list[k]['eta']) < 60),
    ]):
        return False
    else:
        db.users.update(
            {'_id': uid},
            {'$addToSet': {'tasks': task}},
            safe=True)

        return True


def del_task(uid, task_timestamp, flag='tid'):
    ''' 删除一个待发送的微博 '''
    db.users.update(
        {'_id': uid},
        {'$pull': {'tasks': {flag: task_timestamp}}},
        safe=True
    )
    return True


def get_keywords(uid, k_type='buzz_keywords'):
    """ get keywords , default buzz_keywords """
    usr = db.users.find_one({'_id': uid}, {k_type: 1})
    if usr:
        return usr.get(k_type, [])
    else:
        return []


def set_keywords(uid, keywords=[], k_type='buzz_keywords'):
    """ set keywords ,  default buzz_keywords """
    flag = False
    usr = db.users.find_one({'_id': uid}, {})
    if not all((usr, isinstance(keywords, list))):
        pass
    else:
        db.users.update(
            {'_id': uid},
            {'$set': {k_type: keywords}},
            safe=True)

        flag = True

    return flag


def del_keyword(uid, keywords=[], k_type='buzz_keywords'):
    """ delete keywords , default buzz_keywords """
    flag = False
    usr = db.users.find_one({'_id': uid}, {})
    if not all((usr, isinstance(keywords, list))):
        pass
    else:
        db.users.update(
            {'_id': uid},
            {'$set': {k_type: keywords}},
            safe=True)
        flag = True

    return flag


def get_user_ins():
    ''' get users with ins keyword '''
    users = get_users()
    return [x for x in users if 'ins' in x]


def get_buzz_keywords(uid):
    """ get buzz_keywords """
    usr = db.users.find_one({'_id': uid}, {'buzz_keywords': 1})
    if usr:
        return usr.get('buzz_keywords', [])
    else:
        return []
