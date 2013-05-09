# coding=utf8

from utils import MONGODB_INSTANCE
from utils import get_week_start
from utils import get_month_start
from utils import get_all_start

from influence_dao import get_cur_influence

from celebrity_dao import get_celebrity_followers_quality_distr

from random import shuffle

from datetime import datetime


def get_cur_statistic(uid):
    ''' 获取用户的统计数据 '''
    return MONGODB_INSTANCE.user_statistic.find_one({'_id': uid}) or {}


def get_cur_fb_statistic(fid):
    ''' 获取竞品的统计数据 '''
    return MONGODB_INSTANCE.followbrand_statistic.find_one({'_id': fid}) or {}


def get_followers_location_distr(uid, reftime=None):
    '''获取粉丝地理分布'''
    return get_cur_statistic(uid).get('location', {})


def get_followbrand_flwrs_location_distr(fid, reftime=None):
    '''获取粉丝地理分布'''
    return get_cur_fb_statistic(fid).get('location', {})


def get_followers_gender_distr(uid):
    '''获取账号性别分布'''
    return get_cur_statistic(uid).get('gender', {})


def get_followbrand_flwrs_gender_distr(fid):
    '''获取竞品粉丝性别分布'''
    return get_cur_fb_statistic(fid).get('gender', {})


def get_followers_quality_distr(uid, reftime=None):
    '获取粉丝质量度分布'
    tmp_record = get_cur_statistic(uid).get('quality', {})
    for i in range(100):
        if str(i) not in tmp_record:
            tmp_record.update({str(i): 0})

    return tmp_record


def get_followbrand_flwrs_quality_distr(fid):
    '获取粉丝质量度分布'
    tmp_record = get_cur_fb_statistic(fid).get('quality', {})
    for i in range(100):
        if str(i) not in tmp_record:
            tmp_record.update({str(i): 0})

    return tmp_record.items()


def get_followers_activeness_distr(uid, reftime=None):
    '获取粉丝活跃度分布'
    tmp_record = get_cur_statistic(uid).get('activeness', {})
    for i in range(100):
        if str(i) not in tmp_record:
            tmp_record.update({str(i): 0})

    return tmp_record


def get_followbrand_flwrs_activeness_distr(fid):
    '获取竞品粉丝活跃度分布'
    tmp_record = get_cur_fb_statistic(fid).get('activeness', {})
    for i in range(100):
        if str(i) not in tmp_record:
            tmp_record.update({str(i): 0})

    return tmp_record


def get_followers_tags_distr(uid, reftime=None):
    '''获取粉丝tags分布'''
    return get_cur_statistic(uid).get('tags', {})


def get_followbrand_flwrs_tags_distr(fid):
    '''获取竞品粉丝tags分布'''
    return get_cur_fb_statistic(fid).get('tags', {})


def get_followers_verified_distr(uid, reftime=None):
    '''获取粉丝tags分布'''
    return get_cur_statistic(uid).get('verified', {})


def get_followbrand_flwrs_verified_distr(fid):
    '''获取粉丝tags分布'''
    return get_cur_fb_statistic(fid).get('verified', {})


def get_celebrity_followers_quality_distr(uid):
    '''获取名人粉丝质量度分布'''
    result = []
    quality_distr = MONGODB_INSTANCE.celebrity.find_one({'celebrity_id':uid})

    if quality_distr:
        result = quality_distr.get("quality_ratio", {}).items()
    else:
        pass

    return result


def get_last_login_time_records(admaster_user):
    results = MONGODB_INSTANCE.login_time_records.find({
        "user_id":admaster_user.id
    }).sort("at", -1).limit(1)

    if results.count():
        return results[0]
    else:
        return None


def save_login_time_records(admaster_user):
    ''' 保存一条登陆记录 '''
    now = datetime.now()
    record = get_last_login_time_records(admaster_user)

    if any([
        not record,
        (now-record['at']).seconds >= 5*60,
    ]):
        MONGODB_INSTANCE.login_time_records.insert(
            {
                "user_id": admaster_user.id,
                 "name": admaster_user.username,
                 "at":now,
            },
            safe=True,
        )


def get_hotwords_graph(
    uid,
    total_count=30,
    search_from="mentions_hotwords",
    flag='only',
):
    ''' 获取一个账号的评论高频词列表 '''
    hotwords = MONGODB_INSTANCE[search_from].find_one({
        'sm_user_id': uid,
        'f_date': get_all_start(),
        'type': 'all',
    })

    result_list = getattr(hotwords, 'get', lambda x, y:[])('statistic', [])

    if result_list:
        tmp_result_list = [
            {
                "direction": cur_word, 
                "value": int(float(cur_count)/result_list[0][1] * 100),
                "description" : cur_count, 
            }
            for (cur_word, cur_count, cur_o, cur_r) in result_list[:total_count]
        ]
    else:
        tmp_result_list = []

    shuffle(tmp_result_list)
    if flag == 'only':
        return tmp_result_list
    else:
        result_dict = {'data': tmp_result_list}
        return result_dict


def get_hotwords_search(
    uid,
    h_type='all',
    total_count=10,
    search_from='buzz_hotwords',
):
    '''
        获取热词记录
        input:
            - uid: user id
            - h_type: week, month, all
            - total_count: 10, 25
            - search_from: buzz_hotwords, mention_hotwords,
                            directmsg_hotwords
        output:
            - [(, , ), (, , )...]
    '''
    search_dict = {
        'week': get_week_start, 
        'month': get_month_start,
        'all': get_all_start,
    }

    hotwords = MONGODB_INSTANCE[search_from].find_one({
        'sm_user_id': uid,
        'f_date': search_dict[h_type](),
        'type': h_type
    })

    try:
        result_list = hotwords.get('statistic', [])
    except AttributeError:
        result_list = []

    return result_list[:total_count]


def get_fans_quality_distr(uid):
    ''' 获取粉丝的质量度分布 '''
    d = get_followers_quality_distr(uid).items()
    d.sort(key=lambda x: int(x[0]))
    sum_count = sum(map(lambda x: x[1], d)) or 1

    title_list = ['低质量用户(0-25)', '普通用户(25-50)', '高质量用户(50-75)', '骨灰用户(75-100)']
    val_list = [
        '%0.1f' % (sum(map(lambda x: x[1], d[:25])) * 100.0 / sum_count),
        '%0.1f' % (sum(map(lambda x: x[1], d[25:50])) * 100.0 / sum_count),
        '%0.1f' % (sum(map(lambda x: x[1], d[50:75])) * 100.0 / sum_count),
        '%0.1f' % (sum(map(lambda x: x[1], d[75:])) * 100.0 / sum_count),
    ]

    return '\\n'.join([
        ','.join(title_list),
        ','.join(val_list)
    ])


def get_fans_activeness_data(uid):
    d = get_followers_activeness_distr(uid).items()
    d.sort(key=lambda x:int(x[0]))
    sum_count = sum(map(lambda x: x[1], d)) or 1

    title_list = ['不活跃(0-40)', '普通用户(40-60)', '活跃用户(60-75)', '高活跃用户(75-100)']
    val_list = [
        '%0.1f' % (sum(map(lambda x: x[1], d[:40])) * 100.0 / sum_count),
        '%0.1f' % (sum(map(lambda x: x[1], d[40:60])) * 100.0 / sum_count),
        '%0.1f' % (sum(map(lambda x: x[1], d[60:75])) * 100.0 / sum_count),
        '%0.1f' % (sum(map(lambda x: x[1], d[75:])) * 100.0 / sum_count),
    ]

    return '\\n'.join([
        ','.join(title_list),
        ','.join(val_list)
    ]) 


def get_fans_activeness_distr_data(uid, step_length=10):
    d = get_followers_activeness_distr(uid).items()
    d.sort(key=lambda x:int(x[0]))
    data = []
    dlen = len(d) / step_length
    num = 0

    sum_count = sum(map(lambda x: x[1], d))
    
    for n in range(dlen):
        s = sum(map(lambda x: x[1], d[n*step_length:][:step_length]))
        data.append("%s-%s;%0.1f" % (num, num+step_length, 100 * float(s) / max(1.0 , sum_count)))
        num += step_length 
    
    tmp_data = [x.split(';') for x in data]
    return '\\n'.join([
        ','.join([x for (x, y) in tmp_data]),
        ','.join([y for (x, y) in tmp_data])
    ])


def get_fans_quality_data(uid, step_length=10, flwrs_type=None):
    ''' 获取粉丝的质量度信息 '''
    data = []
    num = 0

    if not flwrs_type:
        d = get_followers_quality_distr(uid).items()
    else:
        uid_tmp = convert_uid(uid)
        if flwrs_type == 'celebrity':
            d = get_celebrity_followers_quality_distr(uid_tmp)
        elif flwrs_type == 'followbrand':
            d = get_followbrand_flwrs_quality_distr(uid_tmp)
        else:
            d = []

    d.sort(key=lambda x: int(x[0]))
    sum_count = sum(map(lambda x: x[1], d)) or 1

    for n in range(len(d)/step_length):
        s = sum(map(lambda x: x[1], d[n*step_length:][:step_length]))
        data.append(
            "%s-%s;%0.1f" % (
                num,
                num+step_length,
                100 * float(s) / sum_count,
            )
        )
        num += step_length

    tmp_data = [x.split(';') for x in data]

    return '\\n'.join([
        ','.join([x for (x, y) in tmp_data]),
        ','.join([y for (x, y) in tmp_data]),
    ])


