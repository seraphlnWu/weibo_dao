# coding=utf8
from weibo_dao.dao.utils import get_hbase_instance
from weibo_dao.parser.parser import ModelParser

from config import HBASE_HOST
import happybase


''' base class for data query.  '''

class ResultList(list):
    ''' the return datastructure '''

class BaseQuery(object):
    ''' base class for data query '''

    tb_name = ''
    
    def __init__(self, hbase_host=HBASE_HOST, autoconnect=True, compat='0.92'):
        ''' init func '''
        self.hbase_host = hbase_host
        self.autoconnect = autoconnect
        self.compat = compat

        self.m_parser = ModelParser()
        self.model = self.m_parser.get_model(self.tb_name)
        self.connection = None


    def init_table(self):
        if not getattr(self, 'table', None):
            self.connection = happybase.Connection(
                self.hbase_host,
                autoconnect=self.autoconnect,
                compat=self.compat,
            )
            self.table = self.connection.table(self.tb_name)
    
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
        self.init_table()
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
        self.init_table()
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

        self.init_table()
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
        self.init_table()
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
        self.init_table()
        column = self._convert_column_name([column])[0]
        return self.table.counter_inc(row, column, value)


    def counter_dec(self, row, column, value=1):
        self.init_table()
        column = self._convert_column_name([column])[0]
        return self.table.counter_dec(row, column, value)

    def counter_get(self, row, column):
        """
        Retrieve the current value of a counter column. This method retrieves
        the current value of a counter column. If the counter column does not
        exist, this function initialises it to 0. Note that application code
        should never store a incremented or decremented counter value
        directly; use the atomic
        @row (str) – the row key
        @column (str) – the column name
        """
        self.init_table()
        return self.table.counter_get(row, column)
        
    def exist(self, id):
        '''
        check the given id if already exists, subclass can rewrite
        this method to fetch primary key to save io cost.
        @id(str) - the row key
        '''
        record = self.query_one(id=id)
        return True if record else False


    def _convert_column_name(self, columns):
        '''
        convert general column name to hbase column names
        '''
        return [self.model.columns_dct[c]['column_name']
                for c in columns if c in self.model.columns_dct]

    def close(self):
        ''' close the connection '''
        self.connection.close()
