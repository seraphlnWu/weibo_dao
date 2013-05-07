# coding=utf8

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
