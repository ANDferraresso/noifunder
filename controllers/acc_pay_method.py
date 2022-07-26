from datetime import datetime
import json
import core.controller as ctr
import core.form
import core.render
import core.paginator
import models.db.acc_pay_method
import models.tables.acc_pay_method

ROWS_PER_PAGE = 50

#
class Acc_Pay_Method(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)

        # acc_pay_method
        f = open("dictios/tables/acc_pay_method" + "_" + self.tmpl_vars['cr']['lang'] + ".json", "r")
        self.tmpl_vars['lc']['acc_pay_methodTab'] = {
            "T": json.loads(f.read()),
            "data": [],
            "hasData": False
        }
        f.close()
        self.acc_pay_methodMd = models.db.acc_pay_method.Acc_Pay_Method(
            "sqlite", sqlite_conn,
            models.tables.acc_pay_method.items, "")

        self.form = core.form.Form(self.ctx)
        self.render = core.render.Render()
        self.paginator = core.paginator.Paginator(self.ctx)

    #
    def list_all(self, start_response):
        template_name = "acc_pay_method/list"
        par_page = int(self.ctx['params']['page'])

        order_by, order_prog, self.tmpl_vars['lc']['order_prog'] = self.manage_list_order([
            "rid", "name"
        ])

        ext_refs = False
        quick_list = ["rid", "name"]
        conds = []
        limit = ROWS_PER_PAGE
        offset = 0

        # Filtri
        options = {}
        conds, filter_arr, filters_js, self.tmpl_vars['lc']['filterHTML'] = self.paginator.manage_filter(
            "sqlite", self.acc_pay_methodMd, 
            ext_refs, quick_list, conds, options,
            self.tmpl_vars['cr']['links']['acc_pay_method_list'] + "/1" + "?", 
            "acc_pay_method_filter_btn", 3
        )
        self.tmpl_vars['cr']['js'] += filters_js
        self.tmpl_vars['lc']['list_qs'] = self.manage_list_query_string(order_by, order_prog, filter_arr)
        
        self.tmpl_vars['lc']['acc_pay_methodTab']['filtered'] = False
        if len(filter_arr) > 0:
            self.tmpl_vars['lc']['acc_pay_methodTab']['filtered'] = True
        order = []
        self.tmpl_vars['lc']['acc_pay_methodTab']['rowsNum'] = self.acc_pay_methodMd.select(True, ext_refs, quick_list,
            conds, [], None, 0, {})['data'][0]
        if self.tmpl_vars['lc']['acc_pay_methodTab']['rowsNum'] < 1:
            if par_page != 1:
                # Il numero di pagina è valido, ma la pagina non esiste.
                template_name = "_alerts/page_error"
            self.tmpl_vars['lc']['pagHTML'] = ""
        else:
            pag_pars = {}
            pag_pars.update(filter_arr)
            if order_by != "":
                pag_pars['order_by'] = order_by
                pag_pars['order_prog'] = order_prog
            self.tmpl_vars['lc']['pagHTML'] = self.paginator.pag_html(
                self.tmpl_vars['lc']['acc_pay_methodTab']['rowsNum'], ROWS_PER_PAGE, par_page, '', pag_pars, 'U')
            if par_page < 1 or par_page > self.paginator.pages_num:
                template_name = "_alerts/page_error"
            else:
                order = [["name", "ASC"]]
                if order_by != "":
                    order = [[order_by, order_prog]]  
                offset = (par_page - 1) * ROWS_PER_PAGE
                self.tmpl_vars['lc']['acc_pay_methodTab']['data'] = self.acc_pay_methodMd.select(False,
                    ext_refs, quick_list, conds, order, limit, offset, {})['data']
                if len(self.tmpl_vars['lc']['acc_pay_methodTab']['data']) > 0:
                    self.tmpl_vars['lc']['acc_pay_methodTab']['hasData'] = True

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def create(self, start_response):
        template_name = "acc_pay_method/create"

        ext_refs = True
        quick_list = ["name"]
        not_required = []
        prefix = ''
        self.form.import_table(
            self.acc_pay_methodMd.get_table_def(), self.tmpl_vars['lc']['acc_pay_methodTab']['T'],
            ext_refs, quick_list, not_required, prefix
        )

        display = [
            ["name", 12], 
            ["_csrf", None]
        ]

        form_attrs = {"method": 'post', "novalidate": None}
        before_form_closing = ''
        csrf_value = self.generate_csrf_token()
        self.form.form_def['ui']['_csrf']['attrs']['value'] = csrf_value

        if self.tmpl_vars['env']['METHOD'] == 'GET':
            # GET
            self.tmpl_vars['cr']['method_GET'] = True
            self.set_csrf_cookie(csrf_value)
            f_values = {}
            wrong_fields = []
            use_defaults = True
            after_submit = False
            self.tmpl_vars['lc']['acc_pay_methodTab']['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']['acc_pay_methodTab']['T'], 
                display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                "", self.tmpl_vars['cr']['T']['btn_Send']
            )
            self.tmpl_vars['cr']['js'] += js

            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        elif self.tmpl_vars['env']['METHOD'] == "POST":
            # POST
            self.tmpl_vars['cr']['method_POST'] = True

            # Verifica il token csrf
            if self.validate_csrf_token() is False:
                template_name = "_alerts/csrf_error"
                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

            # Controlla il form        
            f_values, wrong_fields = self.form.validate_all()

            if len(wrong_fields) > 0:
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
            
            # Gestione not_required
            # ...

            # Gestione None
            # ...

            # Verifica opzioni
            # ...

            if len(wrong_fields) == 0:
                ps = {
                    "name": f_values['name'],
                    "creator_rid": 1, 
                    "creation_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    
                }
                location = self.tmpl_vars['cr']['links']['acc_pay_method_list'] + "/1"
                res = self.acc_pay_methodMd.insert(ps)
                self.close_controller()
                if res['err'] == True:
                    self.tmpl_vars['cr']['db_msg'] = res['msg']
                    template_name = "_alerts/db_error"
                    self.close_controller()
                    return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
                else:
                    location = self.tmpl_vars['cr']['links']['acc_pay_method_read'] + "/" + str(res['data'][0])
                    self.close_controller()
                    start_response('302 Found', [('Location', location)])
                    return []
            else:
                self.set_csrf_cookie(csrf_value)
                f_values['_csrf'] = csrf_value
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
                self.tmpl_vars['lc']['acc_pay_methodTab']['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']['acc_pay_methodTab']['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
    
    #
    def read(self, start_response):
        template_name = "acc_pay_method/read"
        
        ext_refs = False
        quick_list = []
        conds = [
            ['W', 'AND', self.acc_pay_methodMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        res =  self.acc_pay_methodMd.select(False, ext_refs, quick_list, conds, order, 1, 0, {})
        print(res)
        self.tmpl_vars['lc']['acc_pay_methodTab']['data'] = self.acc_pay_methodMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        
        if len(self.tmpl_vars['lc']['acc_pay_methodTab']['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        # Payment Method
        self.tmpl_vars['lc']['acc_pay_methodTab']['rendered'] = ""
        self.tmpl_vars['lc']['acc_pay_methodTab']['hasData'] = True
        f_key_links = {}
        fields_to_html_escape = []
        self.tmpl_vars['lc']['acc_pay_methodTab']['rendered'] = self.render.render_record(
            self.acc_pay_methodMd.get_table_columns_keys(),
            self.acc_pay_methodMd.get_table_fKeys(),
            self.tmpl_vars['lc']['acc_pay_methodTab']['T'], 
            self.tmpl_vars['lc']['acc_pay_methodTab']['data'],
            ext_refs, f_key_links, quick_list, fields_to_html_escape, 1
        )

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)


    #
    def update(self, start_response):
        template_name = "acc_pay_method/update"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def delete(self, start_response):
        template_name = "acc_pay_method/delete"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)