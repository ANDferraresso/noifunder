import core.controller as ctr

#
class Root(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)
        pass
        
    #
    def home(self, start_response):
        template_name = "home"

        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)