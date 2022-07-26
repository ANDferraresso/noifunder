import mimetypes
import os.path
import sqlite3
from urllib import parse
from wsgiref import simple_server, util
# Config
import config.setting
# Core
import core.controller
import core.mux
# Controllers
import controllers.alert
import controllers.root
import controllers.acc_gift
import controllers.acc_pay_method
import controllers.act_campaign
import controllers.act_project
import controllers.adm_country
import controllers.adm_editor
import controllers.crm_donor

# Routing
import dictios.routes.url_dictio
import routing.routes

#
def render_error(start_response, msg):
    response_body = [ msg ]
    response_body = "".join(response_body)
    status = "500 Internal server error"
    response_headers = [
        ('Content-type', 'text/plain;charset=UTF-8')
    ]
    # Response
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]


# File statici
def serve_static(start_response, wsgi_env, conf):
    url_file_path = wsgi_env['PATH_INFO'][len(conf['static_dir']):]
    os_file_path = os.path.join(conf['static_path'], url_file_path.lstrip("/"))
    if os.path.exists(os_file_path) and os.path.isfile(os_file_path):
        file_type = mimetypes.guess_type(os_file_path)[0]
        start_response('200 OK', [('Content-Type', file_type)])
        return util.FileWrapper(open(os_file_path, "rb"))
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not found']

# App
def application(environ, start_response):
    # File di configurazione
    conf = config.setting.items

    # Environment
    wsgi_env = dict(environ.items())

    # Check static_file
    if wsgi_env['PATH_INFO'].startswith(conf['static_dir']):
        return serve_static(start_response, wsgi_env, conf)

    # Connessione a SQLite
    data_sqlite_path = os.path.join("data", conf['db_name']) 
    sqlite_conn = None
    if os.path.exists(data_sqlite_path) and os.path.isfile(data_sqlite_path):
        try:
            sqlite_conn = sqlite3.connect( data_sqlite_path)
            sqlite_conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(e)
            return render_error(start_response, str(e))
            # sys.exit(-1)
    else:
        print("Error - File SQLite does not exist")
        return render_error(start_response, "Error - File SQLite does not exist")
        # sys.exit(-1)

    tmpl_vars = {
        'env': {
            'version': conf['version'],
            'version_date': conf['version_date'],
            'app_name': conf['app_name'],
            'default_lang': conf['default_lang'],
            'lang_in_url': conf['lang_in_url'],
            'debug': conf['debug'],
            'static_url': conf['url_scheme'] + "://" + conf['url_host'] + ":" + conf['url_port'] + conf['static_dir'],
            'db_engine': "sqlite",
            'data_path': os.path.join("data", conf['db_name']),
            'views_dir': conf['views_dir'],
            'views_ext': conf['views_ext'],
            'app_url': conf['url_scheme'] + "://" + conf['url_host'] + ":" + conf['url_port'],
            'METHOD': wsgi_env['REQUEST_METHOD']
        }
    }

    # MUX
    routes = routing.routes.routes_tree
    url_t = dictios.routes.url_dictio.items
    mux = core.mux.Mux(routes, url_t)
    leaf, pars = mux.search_route(wsgi_env, conf)
    context = {
        'found_route': pars['found_route'],
        'params': pars['params'],
        'q_params': pars['q_params'],
        'url_parts': pars['url_parts'],
        "post_vars": {},
        "cookie_path": conf['cookie_path'],
        "cookie_comment": conf['cookie_comment'],
        "cookie_domain": conf['cookie_domain'],
        "cookie_max_age": conf['cookie_max_age'],
        "cookie_secure": conf['cookie_secure'],
        "cookie_version": conf['cookie_version'],
        "cookie_httponly": conf['cookie_httponly'],
        "cookie_samesite": conf['cookie_samesite'],
        "app_parameters": {}
    }

    if "HTTP_COOKIE" in wsgi_env:
        context['HTTP_COOKIE'] = wsgi_env['HTTP_COOKIE']
    else:
        context['HTTP_COOKIE'] = ""
        
    if leaf is None:
        # Non trovato
        ctrl = controllers.alert.Alert(sqlite_conn, context, tmpl_vars, url_t)
        return ctrl.http404(start_response)
    else:
        # Trovato
        # file_path = leaf[2]
        # class_name = leaf[3]
        # func_name = leaf[4]
        if wsgi_env['REQUEST_METHOD'] == "POST":
            content_length = 0
            if wsgi_env['CONTENT_LENGTH'] != "":
                content_length = int(wsgi_env['CONTENT_LENGTH'])

            readbytes = environ['wsgi.input'].read(content_length)
            readstr = readbytes.decode('utf-8')
            context['post_vars'] = dict(parse.parse_qsl(readstr))

        ctrl = eval("controllers." + leaf[2].lstrip("/")[0:-3] + "." + leaf[3] + "(sqlite_conn, context, tmpl_vars, url_t)")
        return eval("ctrl." + leaf[4] + "(start_response)")

# Main cicle
if __name__ == '__main__':
    conf = config.setting.items
    print("... server starting up (using WSGIRefServer())...")
    print("Listening on " + conf['url_scheme'] + "://" + conf['url_host'] + ":" + str(conf['url_port']))
    server = simple_server.make_server(conf['url_host'], int(conf['url_port']), app=application)
    server.serve_forever()