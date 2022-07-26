from doctest import ELLIPSIS_MARKER
from matplotlib.pyplot import table
import mysql
import sqlite3

#
class Orm:
    #
    def __init__(self):
        pass

#
class Table:
    #
    def __init__(self, db_engine, db_conn, table_def, resp_type):
        self.db_engine = db_engine
        self.db_conn = db_conn
        self.table_def = table_def
        self.resp_typee =resp_type
        self.ph = ""
        if db_engine == "mysql":
            self.ph = "%s"
        elif db_engine == "sqlite":
            self.ph = "?"

    #
    def get_table_def(self):
        return self.table_def

    #
    def get_table_name(self):
        return self.table_def['name']

    #
    def get_table_primary(self):
        return self.table_def['primary']

    #
    def get_table_uniques(self):
        return self.table_def['uniques']

    #
    def get_table_columnsInUniques(self):
        return self.table_def['columnsInUniques']

    #
    def get_table_indexes(self):
        return self.table_def['indexes']

    #
    def get_table_fKeys(self):
        return self.table_def['fKeys']

    #
    def get_table_columns(self):
        return self.table_def['columns']

    #
    def get_table_columns_keys(self):
        return list(self.table_def['columns'].keys())

    def get_table_def(self):
        return self.table_def

    def _elab_conds(self, conds):
        w_sql = ""
        h_sql = ""
        binds = []; 
        for cond in conds:
            # W = WHERE
            # H = HAVING
            # Esempio: cond = 'W', 'AND', 'user', 'rid', '=', 2, ''
            # Esempio: cond = 'W', 'AND (', 'user', 'gender", '=', 'M', ')'
            # Esempio: cond = 'W', 'AND', '', 'rid', '=', 2, ''
            # Esempio: cond = 'W', 'AND', '', 'rid', 'IS NULL', '', ''
            # Esempio: cond = 'W', 'AND', '', 'rid', 'IS NOT NULL', '', ''
            if cond[0] == "W":
                if cond[2] != '':
                    w_sql += ' ' + cond[1] + ' `' + cond[2] + '`.`' + cond[3] + '` ' + cond[4]
                else:
                    w_sql += ' ' + cond[1] + ' `' + cond[3] + '` ' + cond[4]
                if cond[4] == "IS NULL" or cond[4] == "IS NOT NULL":
                    w_sql += " " + cond[6]
                else:
                    w_sql += " " + self.ph + " " + cond[6]
                    binds.append(cond[5])
            elif cond[0] == "H":
                if cond[2] != '':
                    h_sql += ' ' + cond[1] + ' `' + cond[2] + '`.`' + cond[3] + '` ' + cond[4]
                else:
                    h_sql += ' ' + cond[1] + ' `' + cond[3] + '` ' + cond[4]
                if cond[4] == "IS NULL" or cond[4] == "IS NOT NULL":
                    h_sql += " " + cond[6]
                else:
                    h_sql += " " + self.ph + " " + cond[6]
                    binds.append(cond[5])

        if h_sql != "":
            h_sql = " HAVING 1 " + h_sql

        return w_sql, h_sql, binds 

    # 
    def select(self, count, ext_refs, quick_list, conds, order, limit, offset, pars={}):
        str_distinct = ""
        if "distinct" in pars and pars['distinct'] == True:
            str_distinct = "DISTINCT "

        table_cls = self.table_def['columns'].keys()
        columns = []
        if len(quick_list) > 0:
            columns = quick_list
        else: 
            for v in table_cls:
                columns.append(v)

        if not ext_refs:
            sql = ""
            if count:
                w_cond_sql, h_cond_sql, binds = self._elab_conds(conds)
                if "rid" in table_cls: 
                    if self.db_engine == "mysql":
                        sql = "SELECT COUNT(*) FROM (SELECT `rid` FROM `" + self.table_def['name'] \
                            + "` WHERE 1 " + w_cond_sql + " " + h_cond_sql + ") AS `CNT`"
                    elif self.db_engine == "sqlite":
                        sql = "SELECT COUNT(*) AS `CNT` FROM (SELECT `rid` FROM `" + self.table_def['name'] \
                            + "` WHERE 1" + w_cond_sql + " " + h_cond_sql + ")"
                else:
                    if self.db_engine == "mysql":
                        sql = "SELECT COUNT(*) FROM (SELECT * FROM `" + self.table_def['name'] \
                            + "` WHERE 1 " + w_cond_sql + " " + h_cond_sql + ") AS `CNT`"
                    elif self.db_engine == "sqlite":
                        sql = "SELECT COUNT(*) AS `CNT` FROM (SELECT * FROM `" + self.table_def['name'] \
                            + "` WHERE 1 " + w_cond_sql + " " + h_cond_sql + ")"
            else:
                pass
                # SELECT
                select_sql = ""
                for v in columns:
                    select_sql += "`" + v + "`, "
                select_sql = select_sql.rstrip(", ")
                # WHERE (condizioni)
                w_cond_sql, h_cond_sql, binds = self._elab_conds(conds)
                # ORDER
                order_sql = ""
                if len(order) == 0:
                    order_sql = "1"
                else:
                    for ord in order:
                        order_sql += "`" + self.table_def['name'] + "`.`" + ord[0] + "` " + ord[1] + ", "
                    order_sql = order_sql.rstrip(", ")
                if limit == None:
                    sql = "SELECT " + str_distinct + select_sql + " FROM `" + self.table_def['name'] + "` WHERE 1 " + w_cond_sql + " " + h_cond_sql \
                        + " ORDER BY " + order_sql
                else:
                    sql = "SELECT " + str_distinct + select_sql + " FROM `" + self.table_def['name'] + "` WHERE 1 " + w_cond_sql + " " + h_cond_sql \
                        + " ORDER BY " + order_sql + " LIMIT " + str(offset) + ", " + str(limit)

            # Lancia query
            if self.db_engine == "sqlite":
                # sqlite
                try:
                    cur = self.db_conn.cursor()
                    cur.execute(sql, binds)
                    if count:
                        row = cur.fetchone()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': [int(row['CNT'])]}
                    else:
                        rows = cur.fetchall()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': rows}
                except sqlite3.Error as e:
                    if count:
                        return {'err': True, 'msg': e.args[0], 'data': [0]}
                    else:
                        return {'err': True, 'msg': e.args[0], 'data': []}
            elif self.db_engine == "mysql":
                # mysql
                try:
                    cur = self.db_conn.cursor()
                    cur.execute(sql, binds)
                    if count:
                        row = cur.fetchone()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': [int(row['CNT'])]}
                    else:
                        rows = cur.fetchall()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': rows}
                except mysql.connector.Error as e:
                    if count:
                        return {'err': True, 'msg': e.args[0], 'data': [0]}  
                    else:
                        return {'err': True, 'msg': e.args[0], 'data': []}   
             
        else:
            # ext_refs = TRUE
            # Trova ripetizioni e copia array
            f_keys = {}
            tables_arr = {self.table_def['name']: 1}
            for k in self.table_def['fKeys']:
                v = self.table_def['fKeys'][k]
                if k in columns:
                    if v['toTable'] in tables_arr:
                        tables_arr[ v['toTable'] ] += 1
                    else:
                        tables_arr[ v['toTable'] ] = 1
                    f_keys[k] = v
            #
            for k in tables_arr:
                v = tables_arr[k]
                if v > 1:
                    c = 1
                    for k1 in f_keys:
                        v1 = f_keys[k1]
                        if k == v1['toTable']:
                            f_keys[k1]['toTable'] += "_" + str(c)
                            c += 1
            
            # FROM
            from_sql = ""
            for k in tables_arr:
                v = tables_arr[k]
                if v == 1:
                    from_sql += " `" +  k  + "`, "
                else:
                    c = 1
                    while c <= v:
                        from_sql += " `" + k + "` AS `" +  k  + "_" + str(c) + "`, "
                        c += 1
            from_sql = from_sql.rstrip(", ")

            # SELECT
            select_sql = ""
            where_sql = ""
            # having_sql = ""
            for v in columns:
                if not v in f_keys:
                    select_sql += "`" + self.table_def['name'] + "`.`" + v + "`, "
                else:
                    f_key = f_keys[v]
                    if self.db_engine == "sqlite":
                        select_sql += "`" + self.table_def['name'] + "`.`" + v + "`, "
                        for x in f_key['toRefs']:
                            select_sql += "`" + f_key['toTable'] + "`.`" + x + "` || \" \" || "
                        select_sql = select_sql.rstrip(" || \" \" || ")
                        select_sql += ' AS `' + v + "_FK`, "
                    elif self.db_engine == "mysql":
                        select_sql += "`" + self.table_def['name'] + "`.`" + v + "`, CONCAT("
                        for x in f_key['toRefs']:
                            select_sql += "`" + f_key['toTable'] + "`.`" + x + "`, \" \", "
                        select_sql = select_sql.rstrip(", \" \", ")
                        select_sql += ') AS `' + v + "_FK`, "
                    # WHERE (foreign keys)
                    where_sql += " AND `" + self.table_def['name'] + "`.`" + v + "` = `" + f_key['toTable'] + "`.`" + f_key['toColumn'] + "`"
            select_sql = select_sql.rstrip(", ")

            # Condizioni
            w_cond_sql, h_cond_sql, binds = self._elab_conds(conds)

            sql = ""

            if count:
                pass
            else:
                pass

            if count:
                if select_sql == "":
                    if "rid" in table_cls: 
                        if self.db_engine == "mysql":
                            sql = "SELECT COUNT(*) FROM (SELECT `rid` FROM " + from_sql \
                                + " WHERE 1 " + where_sql + w_cond_sql + " " + h_cond_sql + ") AS `CNT`"
                        elif self.db_engine == "sqlite":
                            sql = "SELECT COUNT(*) AS `CNT` FROM (SELECT `rid` FROM " + from_sql \
                                + " WHERE 1 " + where_sql + w_cond_sql + " " + h_cond_sql + ")"
                    else:
                        if self.db_engine == "mysql":
                            sql = "SELECT COUNT(*) FROM (SELECT * FROM " + from_sql \
                                + " WHERE 1 " + where_sql + w_cond_sql + " " + h_cond_sql + ") AS `CNT`"
                        elif self.db_engine == "sqlite":
                            sql = "SELECT COUNT(*) AS `CNT` FROM (SELECT * FROM " + from_sql \
                                + " WHERE 1 " + where_sql + w_cond_sql + " " + h_cond_sql + ")"
                else:
                    if self.db_engine == "mysql":
                        sql = "SELECT COUNT(*) FROM (SELECT " + select_sql + " FROM " + from_sql \
                            + " WHERE 1 " + where_sql + w_cond_sql + h_cond_sql + ") AS `CNT`"
                    elif self.db_engine == "sqlite":
                        sql = "SELECT COUNT(*) AS `CNT` FROM (SELECT " + select_sql + " FROM " + from_sql \
                            + " WHERE 1 " + where_sql + w_cond_sql + h_cond_sql + ")"
            else:
                # ORDER
                order_sql = ""
                if len(order) == 0:
                    order_sql = "1"
                else:
                    for ord in order:
                        if ord[0][0:1] == "`":
                            order_sql += "`" + ord[0] + "` " + ord[1] + ", "
                        else:
                            order_sql += "`" + self.table_def['name'] + "`.`" + ord[0] + "` " + ord[1] + ", "
                    order_sql = order_sql.rstrip(", ")

                if limit == None:
                    sql = "SELECT " + str_distinct + select_sql + " FROM " + from_sql + " WHERE 1 " \
                        + where_sql + " " + w_cond_sql + " " + h_cond_sql + " ORDER BY " + order_sql
                else:
                    sql = "SELECT " + str_distinct + select_sql + " FROM " + from_sql + " WHERE 1 " \
                        + where_sql + " " + w_cond_sql + " " + h_cond_sql + " ORDER BY " + order_sql \
                        + " LIMIT " +  str(offset) + ", " + str(limit)               

            # Lancia query
            if self.db_engine == "sqlite":
                # sqlite
                try:
                    cur = self.db_conn.cursor()
                    cur.execute(sql, binds)
                    if count:
                        row = cur.fetchone()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': [int(row['CNT'])]}
                    else:
                        rows = cur.fetchall()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': rows}
                except sqlite3.Error as e:
                    if count:
                        return {'err': True, 'msg': e.args[0], 'data': [0]} 
                    else:
                        return {'err': True, 'msg': e.args[0], 'data': []}
            elif self.db_engine == "mysql":
                # mysql
                try:
                    cur = self.db_conn.cursor()
                    cur.execute(sql, binds)
                    if count:
                        row = cur.fetchone()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': [int(row['CNT'])]}
                    else:
                        rows = cur.fetchall()
                        cur.close()
                        return {'err': False, 'msg': "", 'data': rows}
                except mysql.connector.Error as e:
                    if count:
                        return {'err': True, 'msg': e.args[0], 'data': [0]} 
                    else:
                        return {'err': True, 'msg': e.args[0], 'data': []} 

    # Insert
    def insert(self, ps):
        columns_sql = ""
        placeholders = ""
        values = []
        for k in ps:
            v = ps[k]
            columns_sql += "`" + k + "`, "
            placeholders += self.ph + ", "
            values.append(v)
        columns_sql = columns_sql.rstrip(", ")
        placeholders = placeholders.rstrip(", ")

        sql = "INSERT INTO `" + self.table_def['name'] + "` (" + columns_sql + ") VALUES (" + placeholders + ")"
        if self.db_engine == "sqlite":
            # sqlite
            try:
                cur = self.db_conn.cursor()
                cur.execute(sql, values)
                lastrowid = cur.lastrowid
                self.db_conn.commit()
                cur.close()
                return {'err': False, 'msg': "", 'data': [lastrowid]}
            except sqlite3.Error as e:
                return {'err': True, 'msg': e.args[0], 'data': []}
        elif self.db_engine == "mysql":
            # mysql
            try:
                cur = self.db_conn.cursor()
                cur.execute(sql, values)
                lastrowid = cur.lastrowid
                self.db_conn.commit()
                cur.close()
                return {'err': False, 'msg': "", 'data': [lastrowid]}
            except mysql.connector.Error as e:
                return {'err': True, 'msg': e.args[0], 'data': []}

    # Update
    def update(self, ps, conds):
        # Colonne  & valori
        ps_sql = ""
        values = []
        for k in ps:
            ps_sql += "`" + k + "` = " + self.ph + ", "
            values.append(ps[k])
        ps_sql = ps_sql.rstrip(", ")   

        # WHERE (condizioni)
        w_cond_sql, h_cond_sql, binds = self._elab_conds(conds)
        sql = "UPDATE `" + self.table_def['name'] + "` SET " + ps_sql + " WHERE 1 " +  w_cond_sql + " " + h_cond_sql
        values = values + binds

        # Lancia query
        if self.db_engine == "sqlite":
            # sqlite
            try:
                cur = self.db_conn.cursor()
                cur.execute(sql, values)
                rowcount = cur.rowcount
                self.db_conn.commit()
                cur.close()
                return {'err': False, 'msg': "", 'data': [rowcount]}
            except sqlite3.Error as e:
                return {'err': True, 'msg': e.args[0], 'data': []}
        elif self.db_engine == "mysql":
            # mysql
            try:
                cur = self.db_conn.cursor()
                cur.execute(sql, values)
                rowcount = cur.rowcount
                self.db_conn.commit()
                cur.close()
                return {'err': False, 'msg': "", 'data': [rowcount]}
            except mysql.connector.Error as e:
                return {'err': True, 'msg': e.args[0], 'data': []}

    # Delete
    def delete(self, conds):
        # WHERE (condizioni)
        w_cond_sql, h_cond_sql, binds = self._elab_conds(conds)
        sql = "DELETE FROM `" + self.table_def['name'] + "` WHERE 1 " + w_cond_sql + " " + h_cond_sql

        # Lancia query
        if self.db_engine == "sqlite":
            # sqlite
            try:
                cur = self.db_conn.cursor()
                cur.execute(sql, binds)
                rowcount = cur.rowcount
                self.db_conn.commit()
                cur.close()
                return {'err': False, 'msg': "", 'data': [rowcount]}
            except sqlite3.Error as e:
                return {'err': True, 'msg': e.args[0], 'data': []}
        elif self.db_engine == "mysql":
            # mysql
            try:
                cur = self.db_conn.cursor()
                cur.execute(sql, binds)
                rowcount = cur.rowcount
                self.db_conn.commit()
                cur.close()
                return {'err': False, 'msg': "", 'data': [rowcount]}
            except mysql.connector.Error as e:
                return {'err': True, 'msg': e.args[0], 'data': []}