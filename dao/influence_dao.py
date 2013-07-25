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


def get_influence_history(uid, period=10, reftime=None, key_dict=None):
    '''
        get user influence history.
        
        @uid => 目标uid
        @period => 默认间隔
        @reftime => 结束时间
        @key_dict => 要查询的key列表
    '''
    today = today_datetime()
    if reftime and reftime < today:
        pass
    else:
        reftime = today

    from_date = reftime - timedelta(period)

    result = []

    '''
    for i in range(period+1):
        tmp_date = from_date + timedelta(days=i)
        tmp_record = MONGODB_INSTANCE.influence.find_one(
            {'id': uid, 'date': tmp_date}
        )
        if tmp_record:
            result.append(tmp_record)
        else:
            pass

    return result
    '''

    if key_dict:
        return MONGODB_INSTANCE.influence.find(
            {
                'id': uid, 
                'date': {'$gte': from_date, '$lte': reftime},
            },
            key_dict,
            ).sort('date', -1)
    else:
        result = MONGODB_INSTANCE.influence.find({
            'id': uid, 
            'date': {'$gte': from_date, '$lte': reftime},
        }).sort('date', -1)

        return get_influence_list(result) 


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
        u_dict,
    )


def multi_inf_histories_data(keyword_list, uid, period=6, to_date=None):
    "集成历史趋势数据"
    his_list = []

    keyword_dict = {
        'influence': '微博影响力',
        'followers_count': '粉丝数',
        'statuses_count': '微博数',
        'sm_flash_factor': '曝光',
        'sm_eyeball_factor': '眼球',
        'nctc': '新增评论',
        'nrpc': '新增转发',
        'nfcnt': '新增粉丝',
    }

    flag = -1
    for kw in keyword_list:
        tmp_result, _flag = get_count_str(
            get_influence_history(
                uid,
                period,
                to_date,
            ),
            kw,
            flag,
        )
        if his_list:
            tmp_list = [keyword_dict[kw]]
            for cur_item in tmp_result.split('\\n'):
                if cur_item:
                    tmp_list.append(cur_item.split(';')[1])
            his_list.append(','.join(tmp_list))
        else:
            tmp_list = ['Categories']
            tmp_v_list = [keyword_dict[kw]]
            for cur_item in tmp_result.split('\\n'):
                if cur_item:
                    tmp_data, tmp_val = cur_item.split(';')
                    tmp_list.append(tmp_data)
                    tmp_v_list.append(tmp_val)
            his_list.append(','.join(tmp_list))
            his_list.append(','.join(tmp_v_list))

        flag = _flag if kw == 'sm_flash_factor' else -1

    if keyword_list[0] == 'nfcnt':
        result_list = []
        for his in his_list:
            result_list.append(','.join(his.split(',')[1:]))
        his_list = result_list
    return '\\n'.join(his_list)


def get_count_str(histories, keyname, flag=-1):
    """
    input:
        - histories ==> [{},{}]
        - keyname ==> 'statuses_count' ,
                        'followers_count' ,
                        'account_activeness'
                        'followers_activeness'
    output:
        - result ==> 'MON;3\n...'
    """
    result = []
    result_list = [
        (
            his.get('date').strftime('%y年%m月%d日'),
            his.get(keyname, 0)
        ) for his in histories
    ]

    for date, count in sorted(result_list):
        if keyname == "influence":
            result.append('%s;%0.0f\\n' % (date, count))
        else:
            result.append('%s;%0.1f\\n' % (date, count))

    return ''.join(result), flag


def get_influence_info(inf_histories, keyword):
    """
    input:
        - histories ==> [{},{}]
        - keyword ==> 'influence' or 'activeness'
    output:
        - result ==> (cur_value, trend)
    """
    if len(inf_histories) == 0:
        return (0, 0)
    elif len(inf_histories) == 1:
        return (inf_histories[0].get(keyword, 0), 0)
    else:
        if keyword == 'influence':
            today_value = round(inf_histories[0].get(keyword, 0))
            yesday_value = round(inf_histories[1].get(keyword, -1))
        elif keyword == 'followers_activeness':
            today_value = round(inf_histories[0].get(keyword, 0) * 100)
            yesday_value = round(inf_histories[1].get(keyword, 0) * 100)

        if not yesday_value:
            return (today_value, 0)
        else:
            return (
                today_value,
                [
                    0,
                    (float(today_value-yesday_value) * 100 / yesday_value),
                ][yesday_value > 0],
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
            'sm_flash_factor': 1,
            'sm_eyeball_factor': 1,
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
