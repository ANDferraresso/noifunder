import core.controller as ctr

#
class Adm_Editor(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)
        pass

    #
    def list_all(self, start_response):
        template_name = "adm_editor/list"
        par_page = int(self.ctx['params']['page'])

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def create(self, start_response):
        template_name = "adm_editor/create"

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def read(self, start_response):
        template_name = "adm_editor/read"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def update(self, start_response):
        template_name = "adm_editor/update"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def delete(self, start_response):
        template_name = "adm_editor/delete"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)