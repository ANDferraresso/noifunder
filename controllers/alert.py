import core.controller as ctr

#
class Alert(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)
        pass

    #
    def http404(self, start_response):
        template_name = "_alerts/404_error"
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "404 Not Found", [], self.cookies)