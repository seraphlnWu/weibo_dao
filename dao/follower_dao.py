# coding=utf8

from datetime import datetime
from datetime import timedelta

from base import BaseQuery

from utils import MONGODB_INSTANCE
from utils import today_datetime


FollowRelation = BaseQuery('follow_relations')
Follower = BaseQuery('followers')

def get_follower_attr(uid, follower_id, attrs):
    """返回针对当前用户的评论数"""
    return FollowRelation.query_one(id='%s_%s' % (uid, follower_id), columns=attrs)


def get_cache_flwr_by_page(
    uid,
    sort_type='followers_count', 
    page=1, 
    records_per_page=10
):
    """
    TODO
    """
    
    page_info = {}

    flwrs = get_flwr_cache(uid, sort_type)
    stlen = 100 if len(flwrs) > 100 else len(flwrs)
    flwrs = flwrs[(page-1)*records_per_page: page*records_per_page]
    
    if stlen % records_per_page:
        page_info['page_totals'] = stlen / records_per_page + 1
    else:
        page_info['page_totals'] = stlen / records_per_page
        
    page = [page, 1][page < 1 or page > page_info['page_totals']]
    page_info['current_page'] = page
    page_info['records_per_page'] = records_per_page
    page_info['pre_page'] = page - 1 if page > 1 else page
    page_info['next_page'] = page + 1 if page < page_info['page_totals'] else page_info['page_totals']
    page_info['sort_type'] = sort_type

    result_list = []
    for flwr in flwrs:
        fid = flwr[1]
        tmp_flwr = MONGODB_INSTANCE.follow_relations.find_one({'user_id': uid, 'follower_id': fid})
        ret = MONGODB_INSTANCE.followers.find_one({'_id': fid})
        if ret:
            tmp_flwr.update({
                'name': ret['name'], 
                'profile_image_url': ret['profile_image_url'], 
                'verified': ret.get('verified'),
                'gender': ret.get('gender'),
                'location': ret.get('location'),
                'id': ret.get('_id'),
                'created_at_': ret.get('created_at'),
            })
        if tmp_flwr:
            tmp_flwr.update({sort_type: flwr[2]})
            result_list.append((flwr[0], tmp_flwr))

    return page_info, result_list
    
def get_flwr_cache(uid, sort_type):
    """
    TODO
    """
    return


def get_new_followers_by_page(
    uid,
    sort_type='all',
    page=1,
    records_per_page=10,
    start_date=None,
    end_date=None,
    default_period=6,
):
    ''' get new followers by influence records '''

    today = today_datetime()
    results = []
    new_f_list = []

    end_date = end_date or today
    start_date = start_date or end_date - timedelta(days=default_period)

    for x in range((end_date-start_date).days+1):
        tmp_date = start_date + timedelta(days=x)
        tmp_inf = MONGODB_INSTANCE.influence.find_one({'id': uid, 'date': tmp_date}) or {}
        new_f_list.extend(tmp_inf.get('new_fans_list', []))

    total_count = len(new_f_list)
    page_sum, rem = divmod(
        total_count,
        records_per_page,
    )

    page_sum += [1, 0][0 == rem]
    fids = new_f_list[(page-1)*records_per_page: (page*records_per_page)]

    if fids:
        for cur_id in fids:
            results.append(FollowRelation.query_one("%s_%s" % (uid, cur_id)))  

    page_info = ({
        'records_per_page': records_per_page,
        'sort_type': sort_type,
        'page_totals': page_sum,
        'total_count': total_count,
        'current_page': int(page),
        'pre_page': page - 1 if page > 1 else page,
        'next_page': page + 1 if page < page_sum else page_sum,
    })

    return page_info, results 
    



def get_followers_by_page(uid, 
    sort_type='all',
    page=1, 
    records_per_page=10, 
    filterdict={}, 
):
    """
    TODO
    """
    
    records_per_page = [records_per_page, 1][records_per_page < 1]

    page_info = {
        'records_per_page': records_per_page,
        'sort_type': sort_type,
    }

    filter_items = {'user_id': uid}
    filter_items.update(filterdict)
    all_follow_relations = MONGODB_INSTANCE.follow_relations.find(filter_items)
    total_count = all_follow_relations.count()
    page_sum, rem = divmod(
        total_count, 
        records_per_page)
    page_sum += [1, 0][0 == rem]
    page = [page, 1][page < 1 or page > page_sum]
    fids = [
        f
        for f in all_follow_relations.skip(
            (page-1) * records_per_page
        ).limit(records_per_page)
    ]

    for fid in fids:
        ret = MONGODB_INSTANCE.followers.find_one({'_id': fid['follower_id']})
        if ret:
            fid.update({
                'name': ret['name'], 
                'profile_image_url': ret['profile_image_url'], 
                'verified': ret.get('verified'),
                'gender': ret.get('gender'),
                'location': ret.get('location'),
                'id': ret.get('_id'),
                'created_at_': ret.get('created_at'),
            })

    page_info.update({
        'page_totals': page_sum,
        'total_count': total_count,
        'current_page': int(page),
        'pre_page': page - 1 if page > 1 else page,
        'next_page': page + 1 if page < page_sum else page_sum,
    })
    return page_info, fids
    
def get_flwr_cache_up_time(uid):
    """
    TODO, wait for map reduce job
    """
    try:
        return MONGODB_INSTANCE.flwr_cache.find_one({'_id': uid}).get('upt')
    except:
        return datetime(2012, 01, 01)

def get_flwr_cache_tsts(uid):
    """
    TODO: wait for map reduce job
    """
    try:
        return MONGODB_INSTANCE.flwr_cache.find_one({'_id': uid}).get('tsts', 0)
    except:
        return 0

def get_flwr_actime_source(uid):
    return MONGODB_INSTANCE.flwr_actime_source.find_one({"_id":uid}) or {}


def get_follower_all(uid, keyword):
    """
    TODO
    """
    inf = map(
        lambda x: (
            x['follower_id'],
            x.get('friends_count', 0),
            x.get('followers_count', 0),
            x.get('statuses_count', 0),
            x.get('comment_count', 0),
            x.get('repost_count', 0),
            x.get('sm_flwr_quality', 0) * 100,
            x.get('activeness', 0) * 100,
        ),
        MONGODB_INSTANCE.follow_relations.find({'user_id': uid}).sort(keyword, -1).limit(50)
    )
    return inf


def save_cur_follow_relation(dao, row_key, data):
    ''' save the given follow_relation '''
    dao.put_one(id=row_key, data=data)


def save_cur_follower(dao, fid, data):
    ''' save the given follower '''
    dao.put_one(id=str(fid), data=data)


def get_followers(uid, limit=1000):
    ''' get user's followers '''
    return FollowRelation.query(row_prefix="%s" % (uid, ), limit=limit)
