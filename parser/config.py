# coding=utf8
'''
    config file for parser
'''

TABLE_DCT = {
    'followers': '%(id)s',
    'follow_relations': '%(user_id)s_%(follower_id)s',
    'comments': '%(sm_user_id)s_%(status_id)s_%(id)s',
    'reposts': '%(sm_user_id)s_%(retweeted_status_id)s_%(id)s',
    'mentions': '%(sm_user_id)s_%(_id)s',
    'mention_users': '%(sm_user_id)s_%(id)s',
    'status': '%(user_id)s_%(id)s',
    'buzz': '%(url)s_%(create_at)s',
}


FOLLOW_RELATIONS_COLUMN_DICT = {
    'uid': {'column_name': 'fr:uid', 'type': 'int'},
    'fid': {'column_name': 'fr:fid', 'type': 'int'},
    'created_at': {'column_name': 'fr:ca', 'type': 'datetime'},
    'followers_count': {'column_name': 'fr:foc', 'type': 'int'},
    'statuses_count': {'column_name': 'fr:sc', 'type': 'int'},
    'friends_count': {'column_name': 'fr:frc', 'type': 'int'},
    'activeness': {'column_name': 'fr:act', 'type': 'float'},
    'sm_flwr_quality': {'column_name': 'fr:sfq', 'type': 'float'},
    'name': {'column_name': 'fr:n', 'type': 'string'},
    'screen_name': {'column_name': 'fr:sn', 'type': 'string'},
    'gender': {'column_name': 'fr:gd', 'type': 'string'},
    'province': {'column_name': 'fr:pr', 'type': 'string'},
    'city': {'column_name': 'fr:ct', 'type': 'string'},
    'location': {'column_name': 'fr:loc', 'type': 'string'},
    'tags': {'column_name': 'fr:t', 'type': 'list'},
    'profile_image_url': {'column_name': 'fr:piu', 'type': 'string'},
    'favourites_count': {'column_name': 'fr:fc', 'type': 'int'},
    'verified': {'column_name': 'fr:vf', 'type': 'boolean'},
    'fme': {'column_name': 'fr:ff', 'type': 'boolean'},
    'bfcnt': {'column_name': 'fr:bf', 'type': 'int'},
    'comment_count': {'column_name': 'fr:cc', 'type': 'int'},
    'repost_count': {'column_name': 'fr:rc', 'type': 'int'},
    'ad_cate': {'column_name': 'fr:acte', 'type': 'float'},
    'ad_sr': {'column_name': 'fr:asr', 'type': 'string'},
    'ad_val': {'column_name': 'fr:avl', 'type': 'float'},
}

FOLLOWERS_COLUMN_DICT = {
    'id': {'column_name': 'fa:fid', 'type': 'int'},
    'sm_update_time': {'column_name': 'fa:ut', 'type': 'datetime'},
    'name': {'column_name': 'fa:n', 'type': 'string'},
    'statuses_created_at': {'column_name': 'fa:sca', 'type': 'datetime'},
    'screen_name': {'column_name': 'fa:sn', 'type': 'string'},
    'gender': {'column_name': 'fa:gd', 'type': 'string'},
    'province': {'column_name': 'fa:pr', 'type': 'string'},
    'city': {'column_name': 'fa:ct', 'type': 'string'},
    'location': {'column_name': 'fa:loc', 'type': 'string'},
    'friends_count': {'column_name': 'fa:frc', 'type': 'int'},
    'statuses_count': {'column_name': 'fa:sc', 'type': 'int'},
    'followers_count': {'column_name': 'fa:foc', 'type': 'int'},
    'tags': {'column_name': 'fa:t', 'type': 'list'},
    'description': {'column_name': 'fa:de', 'type': 'string'},
    'url': {'column_name': 'fa:url', 'type': 'string'},
    'profile_image_url': {'column_name': 'fa:piu', 'type': 'string'},
    'favourites_count': {'column_name': 'fa:fc', 'type': 'int'},
    'created_at': {'column_name': 'fa:ca', 'type': 'datetime'},
    'verified': {'column_name': 'fa:vf', 'type': 'boolean'},
    'avatar': {'column_name': 'fa:av', 'type': 'string'},
    'fme': {'column_name': 'fa:ff', 'type': 'boolean'},
    'vrson': {'column_name': 'fa:vr', 'type': 'string'},
    'online': {'column_name': 'fa:ol', 'type': 'int'},
    'bfcnt': {'column_name': 'fa:bf', 'type': 'int'},
    'sm_uids': {'column_name': 'fa:fu', 'type': 'list'},
    'ad_cate': {'column_name': 'fa:acte', 'type': 'float'},
    'ad_sr': {'column_name': 'fa:asr', 'type': 'string'},
    'ad_val': {'column_name': 'fa:avl', 'type': 'float'},
}

COMMENTS_COLUMN_DICT = {
    'id': {'column_name': 'cm:id', 'type': 'int'},
    'sm_user_id': {'column_name': 'cm:su', 'type': 'int'},
    'user_id': {'column_name': 'cm:ui', 'type': 'int'},
    'user_name': {'column_name': 'cm:un', 'type': 'string'},
    'sct': {'column_name': 'cm:sc', 'type': 'int'},
    'sft': {'column_name': 'cm:frc', 'type': 'int'},
    'ft': {'column_name': 'cm:foc', 'type': 'int'},
    'ct': {'column_name': 'cm:cuc', 'type': 'datetime'},
    'gdr': {'column_name': 'cm:gd', 'type': 'string'},
    'loc': {'column_name': 'cm:loc', 'type': 'string'},
    'vfd': {'column_name': 'cm:vf', 'type': 'boolean'},
    'flw': {'column_name': 'cm:f', 'type': 'boolean'},
    "profile_image_url": {'column_name': 'cm:piu', 'type': 'string'},
    'reply_comment_id': {'column_name': 'cm:rci', 'type': 'int'},
    'text': {'column_name': 'cm:txt', 'type': 'string'},
    'source': {'column_name': 'cm:src', 'type': 'string'},
    'created_at': {'column_name': 'cm:ca', 'type': 'datetime'},
    'status_id': {'column_name': 'cm:sid', 'type': 'int'},
    'buzz_keywords': {'column_name': 'cm:bk', 'type': 'list'},
    'segment': {'column_name': 'cm:seg', 'type': 'list'},
}


REPOSTS_COLUMN_DICT = {
    'id': {'column_name': 'rp:id', 'type': 'int'},
    'sm_user_id': {'column_name': 'rp:ui', 'type': 'int'},
    'user_id': {'column_name': 'rp:rui', 'type': 'int'},
    'user_screen_name': {'column_name': 'rp:rn', 'type': 'string'},
    'text': {'column_name': 'rp:txt', 'type': 'string'},
    'source': {'column_name': 'rp:src', 'type': 'string'},
    'created_at': {'column_name': 'rp:ca', 'type': 'datetime'},
    'retweeted_status_id': {'column_name': 'rp:rsi', 'type': 'int'},
    'user_status_id': {'column_name': 'rp:rusi', 'type': 'int'},
    'screen_name': {'column_name': 'rp:un', 'type': 'string'},
    're_sts_cnt': {'column_name': 'rp:sc', 'type': 'int'},
    're_frds_cnt': {'column_name': 'rp:frt', 'type': 'int'},
    're_flwrs_cnt': {'column_name': 'rp:foc', 'type': 'int'},
    're_cat': {'column_name': 'rp:rca', 'type': 'datetime'},
    're_gen': {'column_name': 'rp:rgd', 'type': 'string'},
    're_loc': {'column_name': 'rp:rloc', 'type': 'string'},
    're_vfd': {'column_name': 'rp:rvf', 'type': 'boolean'},
    're_flw': {'column_name': 'rp:rf', 'type': 'boolean'},
    're_piurl': {'column_name': 'rp:piu', 'type': 'string'},
    'sm_flash_factor': {'column_name': 'rp:fla', 'type': 'float'},
    'sm_eyeball_factor': {'column_name': 'rp:eb', 'type': 'float'},
}

MENTIONS_COLUMN_DICT = {
    'id': {'column_name': 'mt:id', 'type': 'int'},
    'user_id': {'column_name': 'mt:ui', 'type': 'int'},
    'user_screen_name': {'column_name': 'mt:un', 'type': 'string'},
    'sct': {'column_name': 'mt:sc', 'type': 'int'},
    'sft': {'column_name': 'mt:frc', 'type': 'int'},
    'ft': {'column_name': 'mt:foc', 'type': 'int'},
    'ct': {'column_name': 'mt:uc', 'type': 'datetime'},
    'gdr': {'column_name': 'mt:gd', 'type': 'string'},
    'loc': {'column_name': 'mt:loc', 'type': 'string'},
    'vfd': {'column_name': 'mt:vf', 'type': 'boolean'},
    'flw': {'column_name': 'mt:f', 'type': 'boolean'},
    "profile_image_url" : {'column_name': 'mt:piu', 'type': 'string'},
    'text': {'column_name': 'mt:txt', 'type': 'string'},
    'source': {'column_name': 'mt:src', 'type': 'string'},
    'created_at': {'column_name': 'mt:ca', 'type': 'datetime'},
    'in_reply_to_status_id': {'column_name': 'mt:rsi', 'type': 'int'},
    'in_reply_to_user_id': {'column_name': 'mt:rui', 'type': 'int'},
    'in_reply_to_screen_name': {'column_name': 'mt:rn', 'type': 'string'},
    'segment': {'column_name': 'mt:seg', 'type': 'list'},
}

MENTION_USERS_COLUMN_DICT = {
    "city": {'column_name': 'mu:ct', 'type': 'string'},
    "created_at": {'column_name': 'mu:uc', 'type': 'datetime'},
    "description": {'column_name': 'mu:de', 'type': 'string'},
    "domain": {'column_name': 'mu:ud', 'type': 'string'},
    "favourites_count": {'column_name': 'mu:fc', 'type': 'int'},
    "followers_count": {'column_name': 'mu:foc', 'type': 'int'},
    "friends_count": {'column_name': 'mu:frc', 'type': 'int'},
    "gender": {'column_name': 'mu:gd', 'type': 'string'},
    "location": {'column_name': 'mu:loc', 'type': 'string'},
    "name": {'column_name': 'mu:n', 'type': 'string'},
    "profile_image_url": {'column_name': 'mu:piu', 'type': 'string'},
    "province": {'column_name': 'mu:pr', 'type': 'string'},
    "screen_name": {'column_name': 'mu:sn', 'type': 'string'},
    "statuses_count": {'column_name': 'mu:sc', 'type': 'int'},
    "url": {'column_name': 'mu:url', 'type': 'string'},
    "verified": {'column_name': 'mu:vf', 'type': 'boolean'},
    "mention_count": {'column_name': 'mu:mc', 'type': 'int'},
    "is_follower": {'column_name': 'mu:isf', 'type': 'boolean'},
}


STATUS_COLUMN_DICT = {
    'id': {'column_name': 'st:id', 'type': 'int'},
    'user_id': {'column_name': 'st:ui', 'type': 'int'},
    'text': {'column_name': 'st:txt', 'type': 'string'},
    'created_at': {'column_name': 'st:ca', 'type': 'datetime'},
    'favorited': {'column_name': 'st:fc', 'type': 'boolean'},
    'truncated': {'column_name': 'st:tr', 'type': 'boolean'},
    'atcnt': {'column_name': 'st:ac', 'type': 'int'},
    'geo': {'column_name': 'st:geo', 'type': 'string'},
    'in_reply_to_screen_name': {'column_name': 'st:rsn', 'type': 'string'},
    'in_reply_to_status_id': {'column_name': 'st:rsid', 'type': 'int'},
    'in_reply_to_user_id': {'column_name': 'st:rui', 'type': 'int'},
    'source': {'column_name': 'st:src', 'type': 'string'},
    'source_url': {'column_name': 'st:surl', 'type': 'string'},
    'retweeted_status': {'column_name': 'st:rs', 'type': 'string'},
    'retweeted_status_u_id': {'column_name': 'st:rsui', 'type': 'int'},
    'retweeted_status_u_sname': {'column_name': 'st:rsun', 'type': 'string'},
    'retweeted_status_id': {'column_name': 'st:rsi', 'type': 'int'},
    'retweeted_thumbnail_pic': {'column_name': 'st:rtp', 'type': 'string'},
    'retweeted_bmiddle_pic': {'column_name': 'st:rbp', 'type': 'string'},
    'retweeted_original_pic':{'column_name': 'st:rop', 'type': 'string'},
    'thumbnail_pic': {'column_name': 'st:tp', 'type': 'string'},
    'bmiddle_pic': {'column_name': 'st:bp', 'type': 'string'},
    'original_pic': {'column_name': 'st:op', 'type': 'string'},
    'sm_eyeball_factor': {'column_name': 'st:eb', 'type': 'float'},
    'sm_flash_factor': {'column_name': 'st:fla', 'type': 'float'},
    'comment_count': {'column_name': 'st:cc', 'type': 'int'},
    'repost_count': {'column_name': 'st:rc', 'type': 'int'},
    'last_repost_id': {'column_name': 'st:lr', 'type': 'int'},
}


FOLLOWBRAND_FLWR_RELATIONS_COLUMN_DICT = {
    'uid': {'column_name': 'ffr:uid', 'type': 'int'},
    'fid': {'column_name': 'ffr:fid', 'type': 'int'},
    'created_at': {'column_name': 'ffr:ca', 'type': 'datetime'},
    'followers_count': {'column_name': 'ffr:foc', 'type': 'int'},
    'statuses_count': {'column_name': 'ffr:sc', 'type': 'int'},
    'friends_count': {'column_name': 'ffr:frc', 'type': 'int'},
    'activeness': {'column_name': 'ffr:act', 'type': 'float'},
    'sm_flwr_quality': {'column_name': 'ffr:sfq', 'type': 'float'},
    'name': {'column_name': 'ffr:n', 'type': 'string'},
    'screen_name': {'column_name': 'ffr:sn', 'type': 'string'},
    'gender': {'column_name': 'ffr:gd', 'type': 'string'},
    'province': {'column_name': 'ffr:pr', 'type': 'string'},
    'city': {'column_name': 'ffr:ct', 'type': 'string'},
    'location': {'column_name': 'ffr:loc', 'type': 'string'},
    'tags': {'column_name': 'ffr:t', 'type': 'list'},
    'profile_image_url': {'column_name': 'ffr:piu', 'type': 'string'},
    'favourites_count': {'column_name': 'ffr:fc', 'type': 'int'},
    'verified': {'column_name': 'ffr:vf', 'type': 'boolean'},
    'fme': {'column_name': 'ffr:ff', 'type': 'boolean'},
    'bfcnt': {'column_name': 'ffr:bf', 'type': 'int'},
    'comment_count': {'column_name': 'ffr:cc', 'type': 'int'},
    'repost_count': {'column_name': 'ffr:rc', 'type': 'int'},
    'ad_cate': {'column_name': 'ffr:acte', 'type': 'float'},
    'ad_sr': {'column_name': 'ffr:asr', 'type': 'string'},
    'ad_val': {'column_name': 'ffr:avl', 'type': 'float'},

}


BUZZ_COLUMN_DICT = {
    'title': {'column_name': 'bz:t', 'type': 'string'},
    'pan': {'column_name': 'bz:p', 'type': 'float'},
    'brift': {'column_name': 'bz:b', 'type': 'string'},
    'url': {'column_name': 'bz:u', 'type': 'string'},
    'create_at': {'column_name': 'bz:ca', 'type': 'string'},
    'author': {'column_name': 'bz:a', 'type': 'string'},
    'site': {'column_name': 'bz:s', 'type': 'string'},
    'category': {'column_name': 'bz:c', 'type': 'string'},
    'comment_count': {'column_name': 'bz:cc', 'type': 'int'},
    'view_count': {'column_name': 'bz:vc', 'type': 'int'},
    'source': {'column_name': 'bz:src',  'type': 'string'},
    'industry': {'column_name': 'bz:i', 'type': 'string'},
    'src': {'column_name': 'src:s', 'type': 'string'},
}
