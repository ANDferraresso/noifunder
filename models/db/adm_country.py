import core.orm

class Adm_Country(core.orm.Table):
    #
    def __init__(self, db_engine, db_conn, table_def, resp_type):
        super().__init__(db_engine, db_conn, table_def, resp_type)