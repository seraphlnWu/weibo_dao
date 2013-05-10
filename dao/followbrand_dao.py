# coding=utf8
from utils import MONGODB_INSTANCE

from base import BaseQuery

from user_dao import get_fuids

from influence_dao import get_influence_by_date

from statistic_dao import get_followbrand_flwrs_tags_distr
from statistic_dao import get_followbrand_flwrs_location_distr
from statistic_dao import get_followbrand_flwrs_quality_distr
from statistic_dao import get_followbrand_flwrs_gender_distr
from statistic_dao import get_followbrand_flwrs_activeness_distr

from user_dao import get_user

from datetime import datetime


class FollowbrandsDao(BaseQuery):
    tb_name = 'followbrand'


class FollowbrandFlwrRelationsDao(BaseQuery):
    tb_name = 'followbrand_flwr_relations'


class FollowbrandFlwrsDao(BaseQuery):
    tb_name = 'followbrand_flwrs'


def get_cur_fb_statistic(fid):
    ''' get the given statistic info '''
    return db.followbrand_statistic.find_one({'_id': fid})


def get_followbrand(followbrand_id):
    ''' get followbrand by followbrand id '''
    resultdict = MONGODB_INSTANCE.followbrand.find_one({
        'followbrand_id': followbrand_id,
    }) or {}

    resultdict.update({
        'tag_ratio': get_followbrand_flwrs_tags_distr(followbrand_id),
        'location_ratio': get_followbrand_flwrs_location_distr(followbrand_id),
        'quality_ratio': get_followbrand_flwrs_quality_distr(followbrand_id),
        'gender_ratio': get_followbrand_flwrs_gender_distr(followbrand_id),
        'activeness_ratio': get_followbrand_flwrs_activeness_distr(followbrand_id),
    })
    if resultdict.get('url', '').strip() == 'http://1':
        resultdict['url'] = ''

    return resultdict


def get_followbrands(uid, uidlist, sort_type='influence', sort_reverse=-1):
    '''
    input:
        - uid sina微博uid
    output: [{},...]
    ''' 
    fuids = get_fuids(uid)
    followbrand = []
    for fuid in fuids:
        if fuid in uidlist:
            influence_info = list(get_influence_by_date(
                fuid,
                sort_type,
                sort_reverse,
                limit=1,
            ))
            influence_info = influence_info[0] if len(influence_info) > 0 else {}
            user_info = get_user(fuid)

            influence_info['created_at'] = user_info.get("created_at", datetime(2011, 1,1))
            influence_info['url'] = user_info.get("url", "")
            influence_info['profile_image_url'] = user_info.get("profile_image_url", "")
            influence_info['description'] = user_info.get("description", "")
            influence_info['location'] = user_info.get("location", "")
            influence_info['screen_name'] = user_info.get("screen_name", "")
            influence_info['name'] = user_info.get("screen_name", "")
            influence_info['gender'] = user_info.get("gender", {})
            influence_info['verified'] = user_info.get("verified", {})
            influence_info['followbrand_id'] = user_info.get('id', 0)
            influence_info['fans_quality'] = user_info.get("fans_quality", 0)
            influence_info['sm_flwr_quality'] = user_info.get("fans_quality", 0)
            influence_info['fans_activeness'] = user_info.get("followers_activeness", 0)
            influence_info['activeness'] = user_info.get("account_activeness", 0)
        else:
            influence_info = list(get_followbrand_by_date(
                fuid,
                sort_type,
                sort_reverse,
                limit=1,
            ))
            influence_info = influence_info[0] if len(influence_info) > 0 else {}
        followbrand.append(influence_info)
    return followbrand


def get_followbrand_by_date(
    uid,
    sort_type='date',
    sort_reverse=True,
    limit=0,
):
    ''' get influence by limit '''
    if limit:
        return MONGODB_INSTANCE.followbrand.find({'followbrand_id': uid}).sort(sort_type, sort_reverse).limit(limit)
    else:
        return MONGODB_INSTANCE.followbrand.find({'followbrand_id': uid}).sort(sort_type, sort_reverse)


def update_cur_fb_influence(uid, today, u_dict):
    ''' update the followbrand influence record by uid and today '''
    MONGODB_INSTANCE.followbrand_influence.update(
        {
            'id': uid,
            'date': today,
        }
    )
