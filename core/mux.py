import re
from urllib import parse

#
class Mux:
    #
    def __init__(self, routes, url_t):
        # Protected
        self.routes = routes
        self.url_t = url_t

    #
    def search_route(self, wsgi_env, conf):
        found_route = []
        file_path = ""
        class_name = ""
        func_name = ""
        params = {}
        q_params = {}
        url_parts = {}
        
        # Query string come dizionario
        url_parts['query'] = dict(parse.parse_qsl(wsgi_env['QUERY_STRING']))

        uri = wsgi_env['PATH_INFO']
        uri = re.sub("/{2,}", "/", uri) # Gestisce il simbolo / se ripetuto più volte

        # Rimuove eventuali spazi e / da inizio e fine stringa
        uri = uri.strip()
        uri = uri.strip("/")

        # url_parts['path_arr'] Path come array
        url_parts['path_arr'] = uri.split("/")

        # url_parts['path'] Path come stringa
        url_parts['path'] = ""
        if uri != "":
           url_parts['path'] = '/' + uri

        tree = self.routes['ROOT'][1]
        path_arr_len = len(url_parts['path_arr'])
        idx = 0
        leaf = None
        found_route = []
        while idx < path_arr_len and tree != None:
            exit_flag = False
            token_flag = False
            for k in tree:
                # v = tree[k]
                t = url_parts['path_arr'][idx]
                # Verifica se ci sono parametri dentro a < > 
                if len(k) > 2 and k[0] == "<" and k[-1] == ">":
                    if k.find(":") != -1:
                        # C'è espressione regolare
                        parts = k[1:-1].split(":")
                        if parts[0] == "lang" and conf['lang_in_url'] is True:
                            r = '^' + parts[1] + '$'
                            if re.search(r, t):
                                if t in conf['actived_langs'].split("|"):
                                    params['lang'] = t
                                    found_route.append(k)
                                    token_flag = True
                                else:
                                    token_flag = False
                            else:
                                token_flag = False
                        else:
                            r = '^' + parts[1] + '$'
                            if re.search(r, t):
                                params[parts[0]] = t
                                found_route.append(k)
                                token_flag = True
                            else:
                                token_flag = False
                    else:
                        # Non c'è espressione regolare
                        if k[1:-1] == "lang" and conf['lang_in_url'] is True:
                            if t in conf.conf['actived_langs'].split("|"):
                                params['lang'] = t
                                found_route.append(k)
                                token_flag = True
                            else:
                                token_flag = False
                        else:
                            params[k[1:-1]] = t
                            found_route.append(k)
                            token_flag = True
                # Verifica se ci sono parti da tradurre dentro a { } 
                elif len(k) > 2 and k[0] == '{' and k[-1] == '}' and conf['lang_in_url'] is True:
                    try:
                        if self.url_t[params['lang']]['route'][k[1:-1]] == t:
                            found_route.append(k)
                            token_flag = True
                        else:
                            token_flag = False 
                    except:
                        token_flag = False     
                else:
                    if k == t:
                        found_route.append(k)
                        token_flag = True
                    else:
                        token_flag = False
                #
                if token_flag is True:
                    if idx == path_arr_len - 1:
                        # Essere qui significa che anche l'ultimo token corrisponde,
                        # quindi deve verificare il METHOD e la query string.
                        if tree[k][0] == None:
                            pass
                        else:
                            if wsgi_env['REQUEST_METHOD'] in tree[k][0][0].split("|"):
                                leaf = tree[k][0];                         
                                # Attenzione: Non ci possono essere due route uguali a livello di path.
                                # Solo ora avviene il controllo della query string.
                                # Esempio: array("time", "name:[0-9a-zA-Z_]+", "date").
                                queries = tree[k][0][1]
                                for query in queries:
                                    key = query
                                    pos = query.find(":")
                                    regexp = ""
                                    if pos != -1 and len(query) > 2:
                                        key = query[0:pos]
                                        regexp = query[pos + 1:]
                                    #
                                    if key in url_parts['query']:
                                        if regexp != "":
                                            if not re.search('^' + regexp + '$', url_parts['query'][key]):
                                                leaf = None
                                                break
                                        q_params[key] = url_parts['query'][key]
                                    else:
                                        leaf = None
                                        break
                            else:
                                token_flag = False
                        # Ok
                        exit_flag = True
                    else:
                        tree = tree[k][1]
                        break
                else:
                    continue

            if token_flag is False:
                exit_flag = True

            if exit_flag is True:
                break
            else:
                idx += 1

        #
        if leaf == None:
            # Corrispondenza non trovata
            found_route = []
            file_path = ""
            class_name = ""
            func_name = ""
            params = {}
            q_params = {}
            url_parts = {}
           
        return leaf, {
                'found_route': found_route,
                'file_path': file_path,
                'class_name': class_name,
                'func_name': func_name,
                'params':  params,
                'q_params': q_params,
                'url_parts': url_parts
            }
