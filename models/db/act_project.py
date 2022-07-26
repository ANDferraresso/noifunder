import core.orm

class Act_Project(core.orm.Table):
    #
    def __init__(self, db_engine, db_conn, table_def, resp_type):
        super().__init__(db_engine, db_conn, table_def, resp_type)

    # 
    def get_options(self, conds, add_empty_opt):
        quick_list = ["rid", "code", "title"]
        order = [ ["code", "ASC"] ]
        options = []
        res = self.select(False, False, quick_list, conds, order, None, 0, {})
        if res['err'] == True:
            return {"err": True, "msg": res['msg'], "data": []}
        else:
            options = []
            if add_empty_opt:
                options.append( {0: ""} )
            if len(res['data']) > 0:
                for row in res['data']:
                    options.append( {row['rid']: row['code'] + " " + row['title']} )

        return {"err": False, "msg": "", "data": options}