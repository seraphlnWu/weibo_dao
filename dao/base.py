# coding=utf8
import threading
import Queue

import pymongo

from weibo_dao.parser.parser import ModelParser

from config import HBASE_HOST, HBASE_COMPAT, POOL_SIZE
import happybase


class LazyConnectionPool(happybase.ConnectionPool):
    """
    avoid initializing first connection, all connections are lazy
    """
    
    def __init__(self, size, **kwargs):
        if not isinstance(size, int):
            raise TypeError("Pool 'size' arg must be an integer")

        if not size > 0:
            raise ValueError("Pool 'size' arg must be greater than zero")

        self._lock = threading.Lock()
        self._queue = Queue.LifoQueue(maxsize=size)
        self._thread_connections = threading.local()

        connection_kwargs = kwargs
        connection_kwargs['autoconnect'] = False

        for i in xrange(size):
            connection = happybase.Connection(**connection_kwargs)
            self._queue.put(connection)

            
class ResultList(list):
    ''' the return datastructure '''

class BaseQuery(object):
    ''' base class for data query '''

    tb_name = ''

    pool = LazyConnectionPool(POOL_SIZE, host=HBASE_HOST, compat=HBASE_COMPAT)

    def __init__(self, tb_name):
        self.tb_name = tb_name
        self.m_parser = ModelParser()
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

        with self.pool.connection() as conn:
            return self.m_parser.serialized(
                self.tb_name,
                conn.table(self.tb_name).scan(**kwargs),
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

        with self.pool.connection() as conn:            
            return self.m_parser.serialized(
                self.tb_name,
                conn.table(self.tb_name).row(id, **kwargs),
            )

    def put_one(self, id, data, **kwargs):
        '''
        put / update one record
        @id (str) – the row key
        @data (dict) – the data to store
        @timestamp (int) – timestamp (optional)
        '''

        with self.pool.connection() as conn:         
            conn.table(self.tb_name).put(
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
        with self.pool.connection() as conn: 
            conn.table(self.tb_name).delete(id, columns=columns, **kwargs)

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
        with self.pool.connection() as conn: 
            return conn.table(self.tb_name).counter_inc(row, column, value)

    def counter_dec(self, row, column, value=1):
        column = self._convert_column_name([column])[0]
        with self.pool.connection() as conn: 
            return conn.table(self.tb_name).counter_dec(row, column, value)

            
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
        with self.pool.connection() as conn: 
            return conn.table(self.tb_name).counter_get(row, column)


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


    @classmethod
    def close(cls):
        ''' close connections in the pool '''
        for i in range(POOL_SIZE):
            try:
                conn = cls.pool._queue.get(True, 10)
                conn.close()
            except:
                pass
