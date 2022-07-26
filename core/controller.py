import datetime
import http.cookies
import json 
import os.path
import secrets
import re

#
import core.template

#
class Controller:
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        self.cookies = {}
        self.raw_cookies = None
        self.cookies_val_dict = {}
        self.ctx = ctx
        self.tmpl_vars = tmpl_vars
        self.tmpl_vars['cr'] = {
            'db_msg': "",
            'lang': self.tmpl_vars['env']['default_lang'],
            'links': {},
            'js': "",
            'rebuilt_url': self.rebuild_url(),
            'T': {},
        }
        self.tmpl_vars['lc'] = {
            "tmp": {}
        }
        if "lang" in self.ctx['params']:
            self.tmpl_vars['cr']['lang'] = self.ctx['params']['lang']
        self.url_t = url_t

        self.tmpl_vars['cr']['method_GET'] = False
        self.tmpl_vars['cr']['method_POST'] = False
        if self.tmpl_vars['env']['METHOD'] == 'GET':
            self.tmpl_vars['cr']['method_GET'] = True
        if self.tmpl_vars['env']['METHOD'] == 'POST':
            self.tmpl_vars['cr']['method_POST'] = True

        # general T
        self.tmpl_vars['cr']['T'] = {}
        os_file_path = os.path.join("dictios", "main", 'main_' + self.tmpl_vars['cr']['lang'] + '.json')
        if os.path.exists(os_file_path) and os.path.isfile(os_file_path):
            f = open(os_file_path, "r") 
            self.tmpl_vars['cr']['T'] = json.loads(f.read())
            f.close()

        # Links
        links = {}
        os_file_path = os.path.join("routing", 'quick_links_' + self.tmpl_vars['cr']['lang'] + '.json')
        if os.path.exists(os_file_path) and os.path.isfile(os_file_path):
            f = open(os_file_path, "r") 
            links = json.loads(f.read())
            f.close()
        for i in links:
            self.tmpl_vars['cr']['links'][i] = self.tmpl_vars['env']['app_url'] + links[i]
        # Load cookies
        self.raw_cookies = http.cookies.SimpleCookie()
        self.raw_cookies.load( self.ctx['HTTP_COOKIE'] )
        self.cookies_val_dict = { k: v.value for k, v in self.raw_cookies.items() }

        self.tmpl = core.template.Template()

    #
    def close_controller(self):
        pass
        # if self.sqlite_conn:
        #    self.sqlite_conn.close()

        return

    # 
    def get_cookie_value(self, name):
        if name in self.cookies_val_dict:
            return self.cookies_val_dict[name]
        else:
            return None

    #
    def del_cookie(self, name):
        self.set_cookie(name, "", expires="Thu, 01 Jan 1970 00:00:00 GMT")
        return

    # 
    def set_cookie(self, name, value, **args):
        self.cookies[name] = { 
            'value': str(value)
        }
        # expires:
        if "expires" in args:
            self.cookies[name]['expires'] = args['expires']
        else:
            self.cookies[name]['expires'] = ""
        # path
        if "path" in args:
            self.cookies[name]['path'] = args['path']
        else:
            self.cookies[name]['path'] = self.ctx['cookie_path']
        # comment
        if "comment" in args:
            self.cookies[name]['comment'] = args['comment']
        else:
            self.cookies[name]['comment'] = self.ctx['cookie_comment']
        # domain
        if "domain" in args:
            self.cookies[name]['domain'] = args['domain']
        else:
            self.cookies[name]['domain'] = self.ctx['cookie_domain']
        # max-age expires
        if "max_age" in args:
            self.cookies[name]['max-age'] = args['max_age']
            secs = int(args['max_age'])
            dt = datetime.datetime.now() + datetime.timedelta(seconds = secs)
            if not "expires" in args:
                fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
                self.cookies[name]['expires'] = fdt
        else:
            secs = int(self.ctx['cookie_max_age'])
            dt = datetime.datetime.now() + datetime.timedelta(seconds = secs)
            self.cookies[name]['max-age'] = secs
            if not "expires" in args:
                fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
                self.cookies[name]['expires'] = fdt
        # secure
        if "secure" in args:
            self.cookies[name]['secure'] = args['secure']
        else:
            self.cookies[name]['secure'] = self.ctx['cookie_secure']
        # version
        if "version" in args:
            self.cookies[name]['version'] = args['version']
        else:
            self.cookies[name]['version'] = self.ctx['cookie_version']
        # httponly
        if "httponly" in args:
            self.cookies[name]['httponly'] = args['httponly']
        else:
            self.cookies[name]['httponly'] = self.ctx['cookie_httponly']
        # samesite
        if "samesite" in args:
            self.cookies[name]['samesite'] = args['samesite']
        else:
            self.cookies[name]['samesite'] = self.ctx['cookie_samesite']
        
        return

    #
    def set_csrf_cookie(self, value):
        if value is None:
            value = self.generate_csrf_token()
        self.set_cookie("_csrf", value)

    # 
    def generate_csrf_token(self):
        return secrets.token_hex(nbytes=32)

    #
    def validate_csrf_token(self):
        csrf_token = self.get_cookie_value("_csrf")
        if csrf_token is None:
            return False
        if not "_csrf" in self.ctx['post_vars']:
            return False
        if csrf_token == self.ctx['post_vars']['_csrf']:
            return True
        return False

    #
    def rebuild_url(self):
        link = ""
        if len(self.ctx['found_route']) > 0:
            i = 0
            for tok in self.ctx['found_route']:
                if len(tok) > 2 and (tok[0] == "<" and tok[-1] == ">"):
                    link += "/" + self.ctx['url_parts']['path_arr'][i]
                elif len(tok) > 2 and (tok[0] == "{" and tok[-1] == "}"):
                    link += "/" +  self.ctx['url_parts']['path_arr'][i]
                else:
                    link += "/" + tok
                i += 1
            
            if len(self.ctx['url_parts']['query']) > 0:
                link += "?"
                for k in self.ctx['url_parts']['query']:
                    v = self.ctx['url_parts']['query'][k]
                    link += k + "=" + str(v) + "&"
                link = link[0:-1]
            
        return self.tmpl_vars['env']['app_url'] + link

    #
    def make_URL(self, lang, path, query):
        # Gestisci lingua
        if lang == "":
            lang = self.tmpl_vars['cr']['lang']

    
        # Gestisci il simbolo / se ripetuto più volte
        path = re.sub("/{2,}", "/", path) 
        # Rimuovi eventuali spazi e / da inizio e fine stringa
        # Rimuove eventuali spazi e / da inizio e fine stringa
        path = path.strip()
        path = path.strip("/")

        parts = path.split("/")
        ret = ""
        for part in parts:
            if part[0:1] == '{' and part[0:-1] == '}':
                ret += "/" + self.url_t[lang][ part[1:-1] ]
            else:
                if part != "":
                    ret += "/" + part

        # query
        if len(query) > 0:
            ret += '?'
            for k in query.keys():
                v = query[k]
                if str(v) != "":
                    ret += k + "=" + str(v) + "&"
            ret = ret[0:-1]

        return self.tmpl_vars['env']['app_url'] + "/" + lang + ret

    #
    def verify_uniques(self, crud_mode, rid, model, md_tab, values, record_data, wrong_fields):
        for unique in model.get_table_uniques():
            # Effettua la query SOLO se i valori ci sono tutti E se nessuno è in wrong_fields
            conds = []
            flag = False
            for key in unique:
                if key in wrong_fields or not key in values:
                    flag = True
                    conds = []
                    break
                else:
                    conds.append( ['W', "AND", model.get_table_name(), key, '=', values[key], ''] )
            
            if not flag:
                if crud_mode == "C":
                    # Lancia la query
                    res = model.select(True, False, [], conds, [], None, 0, {})
                    if res['err'] == True:
                        pass
                    else:
                        cnt = res['data'][0]
                        if cnt > 0:
                            for key in unique:
                                wrong_fields.append(key)
                                if "msg_DbErrUnique" in self.tmpl_vars['cr']['T']:
                                    md_tab['T']['msg'][key] = self.tmpl_vars['cr']['T']['msg_DbErrUnique']
                                else:
                                    md_tab['T']['msg'][key] = "Unique clause error."
                elif crud_mode == "U":
                    # Se per tutti vale values[...] == record_data[...],
                    # allora significa che non ci sono cambiamenti e quindi non serve effettuare le query.
                    ps_flag = False
                    for key in unique:
                        if values[key] != record_data[key]:
                            ps_flag = True
                            break

                    if ps_flag:
                        # Lancia la query
                        res = model.select(False, False, ["rid"], conds, [], None, 0, {})
                        if res['err'] == True:
                            pass
                        else:
                            if len(res['data']) == 0 or ( len(res['data']) == 1 and int(res['data'][0]['rid']) == rid ):
                                pass # Ok
                            else:
                                for key in unique:
                                    wrong_fields.append(key)
                                    if "msg_DbErrUnique" in self.tmpl_vars['cr']['T']:
                                        md_tab['T']['msg'][key] = self.tmpl_vars['cr']['T']['msg_DbErrUnique']
                                    else:
                                     md_tab['T']['msg'][key] = "Unique clause error."
                    else:
                        pass

        return wrong_fields

    # 
    def check_option(self, key, arr):
        for i in arr:
            if len(i) == 0:
                return False
            else:
                opt_k = list( i.keys() )[0]
                if str(opt_k) == str(key):
                    return True
        return False

    #
    def get_option(self, key, arr):
        for i in arr:
            if len(i) == 0:
                return ""
            else:
                opt_k = list( i.keys() )[0]
                if opt_k == key:
                    return i[opt_k]
                opt_v = i[opt_k]

    #
    def manage_list_order(self, columns):
        # order_by
        order_by = ""
        if "order_by" in self.ctx['url_parts']['query']:
            if self.ctx['url_parts']['query']['order_by'] in columns:
                order_by = self.ctx['url_parts']['query']['order_by']
        # order_prog
        order_prog = "ASC"
        if "order_prog" in self.ctx['url_parts']['query']:
            if self.ctx['url_parts']['query']['order_prog'] in ["ASC", "DESC"]:
                order_prog = self.ctx['url_parts']['query']['order_prog']
        rev_order_prog = "ASC"
        if order_prog == "ASC":
            rev_order_prog = "DESC"
        else:
            pass
        return order_by, order_prog, rev_order_prog

    #
    def manage_list_query_string(self, order_by, order_prog, filter_arr):
        qs = "&"
        for k in filter_arr:
            qs += k + "=" + filter_arr[k] + "&"
        qs = qs.rstrip("&")
        if qs == "&":
            qs = ""
        return qs