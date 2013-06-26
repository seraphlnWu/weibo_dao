# coding=utf8
from bson import ObjectId
from bson.binary import Binary

from weibo_dao.dao.base import BaseQuery
from weibo_dao.dao.utils import MONGODB_INSTANCE
from weibo_dao.dao.comment_dao import Comment
from weibo_dao.dao.repost_dao import Repost
from weibo_dao.dao.utils import paginate

class StatusDao(BaseQuery):
    ''' inherit from base query '''
    tb_name = 'status'

Status = BaseQuery('status')


def save_sent_status(user_name, uid, pic_name, message, upt, cd=None):
    ''' save a status which need to be sent '''
    return MONGODB_INSTANCE.sent_status.insert(
        {
            'uname': user_name,
            'uid': uid,
            'pic_name': pic_name,
            'message': message,
            'upt': upt,
            'cd': cd,
        },
        safe=True,
    )


def update_sent_status_info(sts_id, upt):
    ''' update a to be sent status info '''
    MONGODB_INSTANCE.sent_status.update(
        {
            '_id': ObjectId(sts_id),
        },
        {
            '$set': {
                'sentdate': upt,
            }
        },
        safe=True
    )


def img_save(uid, pic_name, pic_content,content_type="image/png"):
    ''' 保存一张待发的图片 '''
    return MONGODB_INSTANCE.images.insert(
        {
            "uid": uid,
            "pic_name": pic_name,
            "pic_content": Binary(pic_content),
            "content_type": content_type, 
        },
        safe=True,
    )


def img_load(uid, pic_name):
    ''' 根据uid pic获取一张图片 '''
    imgs = MONGODB_INSTANCE.images.find_one({"uid": uid, "pic_name": pic_name})
    return imgs.get('pic_content'), imgs['content_type']


def img_remove(uid, pic_name):
    ''' remove a picture by uid and pic_name '''
    return MONGODB_INSTANCE.images.remove({"uid": uid, "pic_name": pic_name})

def get_status_all(uid):
    """
    TODO
    最近200条微博，map reduce or indexing
    """
    statuses = map(
        lambda x: (
            x.get('id', 0),
            x.get('text', 0), #FIXME x.retweeted_status.text !!
            x.get('created_at', 0),
            x.get('sm_flash_factor', 0),
            x.get('sm_eyeball_factor', 0),
            x.get('comment_count', 0),
            x.get('repost_count', 0),
            ),
        MONGODB_INSTANCE.status.find({'user_id': uid}).sort('created_at', -1)[:200])

    result = []
    
    for sta in statuses:
        result.append((
            sta[1:],
            map(
                lambda x:(
                    x['text'],
                    x.get('user_name', ''),  #FIXME !!
                    x['created_at'],
                    x.get('profile_image_url',
                        '/sm_media/img/default_thumbnail.gif')),
                MONGODB_INSTANCE.comments.find({'status_id': sta[0]}).sort('created_at', -1)
            )
        ))

    return result

def delete_status(uid, status_id):
    """
    set delete flag of status and corresponding
    comments and reposts True
    """

    s_id = '%s_%s' % (uid, status_id)
    Status.put_one(s_id, {'sm_deleted': True})

    for comment in Comment.query(row_prefix=s_id, columns=['id']):
        Comment.put_one('%s_%s' %(s_id, comment['id']), {'sm_deleted': True})

    for repost in Repost.query(row_prefix=id, columns=['id']):
        Repost.put_one('%s_%s' % (s_id, repost['id']), {'sm_deleted': True})


def get_statuses_by_page(
    uid,
    sort_type='created_at',
    page=1,
    records_per_page=10,
    sort_reverse=True,
):
    st_cursor = MONGODB_INSTANCE.status.find({
            'user_id':uid,
    }).limit(page*records_per_page)

    page_info, sts_lst = paginate(
        st_cursor,
        sort_type,
        page,
        records_per_page,
        sort_reverse
    )

    for cur_status in sts_lst:
        if 'scmt' in cur_status:
            cur_status['comment_count'] = cur_status.get('scmt', 0)
        if 'srpt' in cur_status:
            cur_status['repost_count'] = cur_status.get('srpt', 0)

    return page_info, sts_lst
