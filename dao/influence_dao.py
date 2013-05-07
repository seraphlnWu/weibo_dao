# coding=utf8
from datetime import timedelta

from utils import MONGODB_INSTANCE
from utils import today_datetime

from share_method import paginate


def get_cur_influence(uid):
    '获取用户可变属性。eg:影响力，粉丝数，微博数'
    inf_list = MONGODB_INSTANCE.influence.find(
        {'id': uid}
    ).sort('date', -1).limit(10)

    for cur_inf in inf_list:
        if any([
            cur_inf.get('followers_count'),
            cur_inf.get('influence'),
            cur_inf.get('followrs_activeness_distr'),
            cur_inf.get('friends_count'),
            cur_inf.get('statuses_count'),
        ]):
            return cur_inf

    return get_last_influence(uid)


def get_last_influence(uid):
    ''' 获取一条influence记录 '''
    return MONGODB_INSTANCE.influence.find_one({'id': uid}) or {}


def get_influence_history(uid, period=10, reftime=None):
    ''' 获取一个influence历史记录的列表 '''

    today = today_datetime()

    if reftime and reftime < today:
        pass
    else:
        reftime = today

    from_date = reftime - timedelta(period)

    result = MONGODB_INSTANCE.influence.find({
        'id': uid, 
        'date': {'$gt': from_date, '$lte': reftime},
    }).sort('date', -1)

    return check_influence_list(result)


def check_influence_list(histories):
    ''' 检查传入的influence列表中的数据是否合法 '''
    his_list = []
    for his in histories:
        if any([
            his.get('account_activeness', 0),
            his.get('followers_quality', 0),
            his.get('followers_activeness', 0)
        ]):
            if len(his_list) == 0:
                his_list.append(his)
            else:
                if not (his['date'].day - his_list[-1]['date'].day):
                    continue
                else:
                    his_list.append(his)
        else:
            pass

    return his_list


def get_histories_by_page(
    uid,
    sort_type='date',
    page=1,
    records_per_page=10,
    sort_reverse=True,
):

    histories = MONGODB_INSTANCE.influence.find(
        {'id': uid},
        {
            'date': 1,
            'influence': 1,
            'followers_count': 1,
            'statuses_count':1,
            'friends_count': 1,
            'account_activeness': 1,
            'followers_activeness': 1,
            'followers_quality': 1
        }
    )

    #FIXME 没有考虑到可能没有某个关键词的情况
    his_list = sorted(
        get_influence_list(histories),
        key=lambda x:x.get(sort_type, 0),
        reverse=sort_reverse,
    )

    page_info, records = paginate(
        his_list,
        sort_type,
        page,
        records_per_page,
        sort_reverse,
    )

    return page_info, records


def get_influence_by_date(
    uid,
    sort_type='date',
    sort_reverse=True,
    limit=0,
):
    ''' get influence by limit '''
    if limit:
        return MONGODB_INSTANCE.influence.find(
            {'id': uid}
        ).sort(sort_type, sort_reverse).limit(limit)
    else:
        return MONGODB_INSTANCE.influence.find(
            {'id': uid}
        ).sort(sort_type, sort_reverse)


def get_influence_list(histories):
    ''' check the given influence records '''
    his_list = []
    for his in histories:
        if any([
            his.get('account_activeness', 0),
            his.get('followers_quality', 0),
            his.get('followers_activeness', 0)
        ]):
            if len(his_list) == 0:
                his_list.append(his)
            else:
                if not (his['date'].day - his_list[-1]['date'].day):
                    continue
                else:
                    his_list.append(his)
        else:
            continue

    return his_list


def update_cur_influence(uid, today, u_dict):
    ''' update the user influence record by uid and today '''
    MONGODB_INSTANCE.influence.update(
        {
            'id': uid,
            'date': today,
        },
        {"$set": u_dict},
        safe=True,
    )


##############################################################################
# excel files
##############################################################################
def get_histories_for_excel(uid, from_date=None, to_date=None):
    '''
        read the influence history and make an excel stream.
        @uid => the target uid
        @from_date => start date
        @to_date => end date
    '''
    to_date = to_date or today_datetime()

    # default for 1 month
    from_date = from_date or to_date - timedelta(days=30)

    histories = MONGODB_INSTANCE.influence.find(
        {
            'id': uid,
            'date': {
                '$gte': from_date,
                '$lte': to_date,
            }
        },
        {
            'date': 1,
            'influence': 1,
            'account_activeness': 1,
            'followers_quality': 1,
            'followers_activeness': 1,
            'nfcnt': 1,
            'nctc': 1,
            'nrpc': 1,
            'followers_count': 1,
            'statuses_count': 1,
        }
    ).sort('date', -1)
        
    return get_influence_list(histories)


def get_influence_all(uid):
    ''' get 1 month influence records '''
    to_date = today_datetime()
    from_date = to_date - timedelta(days=30)
    inf = map(
        lambda x: (
            x.get('date', from_date),
            x.get('influence', 0),
            x.get('account_activeness', 0) * 100,
            x.get('followers_activeness', 0) * 100,
            x.get('followers_quality', 0) * 100,
        ), get_histories_for_excel(uid)
    )
    return inf


def get_nflwr_all(uid, from_date, to_date):
    to_date = to_date or today_datetime()
    from_date = from_date or to_date - timedelta(days=6)
    inf = map(
        lambda x: (
            x.get('date', ''),
            x.get('nfcnt', 0)
        ), get_histories_for_excel(uid, from_date, to_date)
    )
    return inf 


def get_nctc_nrpc_all(uid, from_date, to_date):
    to_date = to_date or today_datetime()
    from_date = from_date or to_date - timedelta(days=6)
    inf = map(
        lambda x: (
            x.get('date', ''),
            x.get('nctc', 0),
            x.get('nrpc', 0)
        ), get_histories_for_excel(uid, from_date, to_date) 
    )
    return inf 

def get_flash_eyeball_all(uid, from_date, to_date):
    to_date = to_date or today_datetime()
    from_date = from_date or to_date - timedelta(days=6)
    inf = map(
        lambda x: (
            x.get('date', ""),
            x.get('sm_flash_factor', 0),
            x.get('sm_eyeball_factor', 0)
        ), get_histories_for_excel(uid, from_date, to_date)
    )
    return inf 

def get_flash_inf_all(uid, from_date, to_date):
    to_date = to_date or today_datetime()
    from_date = from_date or to_date - timedelta(days=6)
    inf = map(
        lambda x: (
            x.get('date', ""),
            x.get('influence', 0),
            x.get('followers_count', 0),
            x.get('statuses_count', 0),
        ), get_histories_for_excel(uid, from_date, to_date) 
    )
    return inf
