# coding=utf8
from weibo_dao.dao.utils import HBASE_INSTANCE
from weibo_dao.parser.parser import ModelParser

''' base class for data query.  '''

class ResultList(list):
    ''' the return datastructure '''

class BaseQuery(object):
    ''' base class for data query '''

    tb_name = ''
    
    def __init__(self):
        ''' init func '''
        self.m_parser = ModelParser()
        self.table = HBASE_INSTANCE.table(self.tb_name)
        self.model = self.m_parser.get_model(self.tb_name)

    def query(self, **kwargs):
        '''
        query a bunch of results
        @row_start (str) – the row key to start at (inclusive)
        @row_stop (str) – the row key to stop at (exclusive)
        @row_prefix (str) – a prefix of the row key that must match
        @columns (list_or_tuple) – list of columns (optional)
        @filter (str) – a filter string (optional)
        @timestamp (int) – timestamp (optional)
        @include_timestamp (bool) – whether timestamps are returned
        @batch_size (int) – batch size for retrieving results
        @limit (int) - number of records to be fetched
        '''

        if 'columns' in kwargs:
            kwargs['columns'] = self._convert_column_name(kwargs['columns'])

        return self.m_parser.serialized(
            self.tb_name,
            self.table.scan(**kwargs),
        )

    def query_one(self, id, **kwargs):
        '''
        query one result
        @id (str) – the row key
        @columns (list_or_tuple) – list of columns (optional)
        @timestamp (int) – timestamp (optional)
        @include_timestamp (bool) – whether timestamps are returned
        '''
        if 'columns' in kwargs:
            kwargs['columns'] = self._convert_column_name(kwargs['columns'])

        return self.m_parser.serialized(
            self.tb_name,
            self.table.row(id, **kwargs),
        )
    
    def put_one(self, id, data, **kwargs):
        '''
        put / update one record
        @id (str) – the row key
        @data (dict) – the data to store
        @timestamp (int) – timestamp (optional)
        '''
        self.table.put(
            id,
            self.m_parser.deserialized(self.tb_name, data),
            **kwargs
        )

    def delete(self, id, columns=None, **kwargs):
        '''
        delete records
        @id (str) – the row key
        @columns (list_or_tuple) – list of columns (optional)
        @timestamp (int) – timestamp (optional)
        '''
        
        self.table.delete(id, columns=columns, **kwargs)


    def counter_inc(self, row, column, value=1):
        """
        Atomically increment (or decrements) a counter column.
        This method atomically increments or decrements a counter
        column in the row specified by row. If the counter column
        did not exist, it is automatically initialised to 0 before
        incrementing it.

        @row (str) – the row key
        @column (str) – the column name
        @value (int) – the amount to increment or decrement by (optional)
        """
        column = self._convert_column_name([column])[0]
        return self.table.counter_inc(row, column, value)


    def counter_dec(self, row, column, value=1):
        column = self._convert_column_name([column])[0]
        return self.table.counter_dec(row, column, value)

    def exist(self, id):
        '''
            check the given id if already exists.
            @id(str) - the row key
        '''
        record = self.query_one(id=id)
        return True if record else False


    def _convert_column_name(self, columns):
        return [self.model.columns_dct[c]['column_name']
                for c in columns if c in self.model.columns_dct]
