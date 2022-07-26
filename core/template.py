import http.cookies
import json 
import os.path
#
import ext.chevron as chevron

#
class Template:
    #
    def __init__(self):
        pass

    # Render cookies
    def _render_cookies(self, response_headers, cookies):
        for k in cookies.keys():
            sc = http.cookies.SimpleCookie()
            sc[k] = cookies[k]['value']
            sc[k]['expires'] = cookies[k]['expires']
            sc[k]['path'] = cookies[k]['path']
            sc[k]['comment'] = cookies[k]['comment']
            sc[k]['domain'] = cookies[k]['domain']
            sc[k]['max-age'] = cookies[k]['max-age']
            sc[k]['secure'] = cookies[k]['secure']
            sc[k]['version'] = cookies[k]['version']
            sc[k]['httponly'] = cookies[k]['httponly']
            sc[k]['samesite'] = cookies[k]['samesite']
            response_headers.extend(("Set-cookie", morsel.OutputString())
                for morsel in sc.values()
        )
        return response_headers

    #
    def render_page(self, start_response, template_name="", tmpl_vars={}, status="", response_headers=[], cookies={}):
        file_path = tmpl_vars['env']['views_dir'] + "/" + template_name + "." + tmpl_vars['env']['views_ext']
        if os.path.exists(file_path) and os.path.isfile(file_path):
            f = open(file_path, 'r')
            args = {
                'template': f,
                'partials_path': 'views/_partials/',
                'partials_ext': 'mustache',
                'data': tmpl_vars 
            }
            response_body = [
                chevron.render(**args)
            ]
            response_body = "".join(response_body)
            # Status
            if status == "":
                status = "200 OK"
            # Response headers
            if len(response_headers) == 0:
                response_headers = [
                    ('Content-type', 'text/html'),
                ]
            else:
                rh_flag = False
                for rh in response_headers:
                    if rh[0].lower() == 'Content-type'.lower():
                        rh_flag = True
                        break
                    if not rh_flag:
                        response_headers.append(('Content-type', 'text/html'))
            # Cookies
            response_headers = self._render_cookies(response_headers, cookies)
            start_response(status, response_headers)
            return [response_body.encode('utf-8')]
        else:
            f = "File Not Found Error - Template"
            if tmpl_vars['env']['debug']:
                f += " (" + file_path + ")"
            args = {
                'template': f,
                'data': {} 
            }
            response_body = [
                chevron.render(**args)
            ]
            response_body = "".join(response_body)
            status = "500 Internal Server Error"
            response_headers = [
                ('Content-type', 'text/plain'),
            ]
            # Cookies
            response_headers = self._render_cookies(response_headers, cookies)
            # Response
            start_response(status, response_headers)
            return [response_body.encode('utf-8')]

    #
    def render_json(self, start_response, json_str="", status="", cookies={}):
        response_body = [ json_str ]
        response_body = "".join(response_body)
        # Status
        if status == "":
            status = "200 OK"
        response_headers = [
            ('Content-type', 'application/json')
        ]
        # Cookies
        response_headers = self._render_cookies(response_headers, cookies)
        # Response
        start_response(status, response_headers)
        return [response_body.encode('utf-8')]

    #
    def render_text(self, start_response, text="", status="", cookies={}):
        response_body = [ text ]
        response_body = "".join(response_body)
        # Status
        if status == "":
            status = "200 OK"
        response_headers = [
            ('Content-type', 'text/plain;charset=UTF-8')
        ]
        # Cookies
        response_headers = self._render_cookies(response_headers, cookies)
        # Response
        start_response(status, response_headers)
        return [response_body.encode('utf-8')]