# coding=utf8
'''
    utils file.
    just for support functions and connections.
'''

import pymongo
import happybase

from datetime import datetime
from datetime import timedelta
import time

from config import MONGODB_HOST
from config import MONGODB_PORT
from config import MONGODB_DBNAME
from config import HBASE_HOST
from config import APP_TYPE

def get_db(
    mongo_host=MONGODB_PORT,
    mongo_port=MONGODB_PORT,
    mongo_dbname=MONGODB_DBNAME
):
    '''
        get a mongodb instance
    '''
    return pymongo.Connection(MONGODB_HOST, MONGODB_PORT)['sandbox_mongo_5']


def get_hbase_instance(hbase_host=HBASE_HOST, autoconnect=True):
    '''
        get a hbase instance
    '''
    return happybase.Connection(hbase_host, autoconnect=autoconnect, compat='0.92')
    #, compat='0.90')


MONGODB_INSTANCE = get_db()



def today_datetime():
    """ 返回今天的datetime时间 """
    return datetime.strptime(
        '%04d%02d%02d' % (lambda x: (x.year, x.month, x.day))(
            datetime.now()),
        '%Y%m%d')

def compare_value(o_value, default_value, logic_word='and'):
    ''' return o_value if o_value else default_value '''
    result = None
    if logic_word == 'and':
        result = o_value if o_value else default_value
    elif logic_word == 'not':
        result = o_value if not o_value else default_value

    return result


def convert_datetime_to_time(o_datetime):
    ''' convert a datetime object to timestamp '''
    if not isinstance(o_datetime, datetime): 
        raise TypeError, 'The type is not correctly'
    else:
        pass
    return int(time.mktime(o_datetime.timetuple()))


def get_week_start(f_date=None):
    """ 得到这一周的开始时间 """
    if not f_date:
        f_date = today_datetime()

    return f_date - timedelta(f_date.weekday())


def get_month_start(f_date=None):
    """ 得到这个月的开始时间 """
    if not f_date:
        f_date = today_datetime()

    return f_date - timedelta(f_date.day - 1)


def get_all_start():
    """ 所有起始时间 """
    return datetime(2000, 1, 1)


def paginate(
    st_list, 
    sort_type, 
    page, 
    records_per_page, 
    sort_reverse=True
):
    '''
        分页和排序
    '''

    page_info = {}
    if isinstance(st_list, list):
        stlen = len(st_list)
        results = sorted(
            st_list,
            key=lambda x: x.get(sort_type),
            reverse=sort_reverse
        )[(page-1)*records_per_page: page*records_per_page]
    else:
        st_list.sort(sort_type, [1, -1][sort_reverse==True])
        stlen = st_list.count()
        results = st_list[(page-1)*records_per_page: page*records_per_page]

    if stlen % records_per_page:
        page_info['page_totals'] = stlen / records_per_page + 1
    else:
        page_info['page_totals'] = stlen / records_per_page

    page = [page, 1][page < 1 or page > page_info['page_totals']]
    page_info['current_page'] = page
    page_info['records_per_page'] = records_per_page
    page_info['pre_page'] = page - 1 if page > 1 else page
    page_info['sort_type'] = sort_type
    if page < page_info['page_totals']:
        page_info['next_page'] = page + 1
    else:
        page_info['next_page'] = page_info['page_totals']

    return page_info, list(results)

def getLocationList(flwrs_locations):
    """
    input:
        flwrs_location ==> 区域字典
    output:
        flwrs_location_list ==> 经过区域合并后，并排序，交换key和value位置，取top20的list
    """
    temp = {}
    for key in flwrs_locations.keys():
        shortkey = key.encode('utf-8').split(',')[-1].split(' ')[0]
        if temp.has_key(shortkey):
            temp[shortkey] = temp[shortkey] + flwrs_locations[key]
        else:
            temp[shortkey] = flwrs_locations[key]
    flwrs_location_list = map(lambda x:(x[1], x[0]), temp.items())
    flwrs_location_list.sort(reverse = True)
    sum_count = sum(map(lambda x: x[0], flwrs_location_list))

    return map(
        lambda x: ("%.1f" % (100 * float(x[0]) / sum_count), x[1]),
        flwrs_location_list)[0:20]

def get_tags_distr(tags):
 
    flwrs_tags_list = map(lambda x:(x[1], x[0]), tags.items())
    flwrs_tags_list = [
        flwrs_tags_list,
        flwrs_tags_list[0:20]
    ][len(flwrs_tags_list) > 20]

    sum_count = sum(map(lambda x: x[0], flwrs_tags_list))
    
    flwrs_tags_list.sort(reverse=True) 
    tags_distr_str = ''.join(
        map(
            lambda x:x[1] + ';' + str(x[0]) + '\\n',
            map(
               lambda x: ("%.1f" % (100 * float(x[0]) / sum_count), x[1]),
               flwrs_tags_list)
            )
    )
    return tags_distr_str

def loc_str(loc):
    """
    用于地域分布中字符合并的简单函数
    """
    # pattern of loc is {'11,12,北京':1}
    return loc[1].split(",")[-1].split(' ')[0] + ";" + str(loc[0]) + "\\n"

def convert_uid(id_str):
    '''
    根据不同平台转换id
    使用背景是sina与tencent平台的uid类型不一样，sina为int，tencent为str
    '''
    if APP_TYPE == 'SINA':
        return int(id_str)
    else:
        return str(id_str)


def format_date(created_at):
    """ 格式化创建时间 """
    if isinstance(created_at, unicode):
        return datetime.strptime(created_at, '%a %b %d %H:%M:%S +%f %Y')
    else:
        return created_at


def cur_min_datetime():
    return datetime.strptime(
        '%04d%02d%02d%02d%02d' % (
            lambda x: (x.year, x.month, x.day, x.hour, x.minute)
        )(datetime.now()),
        '%Y%m%d%H%M')
