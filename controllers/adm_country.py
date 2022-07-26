from datetime import datetime
import json
import core.controller as ctr
import core.form
import core.render
import core.paginator
import models.db.adm_country
import models.tables.adm_country

ROWS_PER_PAGE = 50

#
class Adm_Country(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)

        # adm_country
        f = open("dictios/tables/adm_country" + "_" + self.tmpl_vars["cr"]["lang"] + ".json", "r")
        self.tmpl_vars["lc"]["adm_countryTab"] = {
            "T": json.loads(f.read()),
            "data": [],
            "hasData": False
        }
        f.close()
        self.adm_countryMd = models.db.adm_country.Adm_Country(
            "sqlite", sqlite_conn,
            models.tables.adm_country.items, "")

        self.form = core.form.Form(self.ctx)
        self.render = core.render.Render()
        self.paginator = core.paginator.Paginator(self.ctx)        

    #
    def list_all(self, start_response):
        template_name = "adm_country/list"
        par_page = int(self.ctx['params']['page'])

        order_by, order_prog, self.tmpl_vars['lc']['order_prog'] = self.manage_list_order([
            "rid", "name", "code", "active", "eu", "currency"
        ])

        ext_refs = False
        quick_list = ["rid", "name", "code", "active", "eu", "currency"]
        conds = []
        limit = ROWS_PER_PAGE
        offset = 0

        # Filtri
        options = {
            "active": self.tmpl_vars['lc']['adm_countryTab']['T']['opts']['active'],
            "eu": self.tmpl_vars['lc']['adm_countryTab']['T']['opts']['eu'],
        }
        conds, filter_arr, filters_js, self.tmpl_vars['lc']['filterHTML'] = self.paginator.manage_filter(
            "sqlite", self.adm_countryMd, 
            ext_refs, quick_list, conds, options,
            self.tmpl_vars['cr']['links']["adm_country_list"] + "/1" + "?", 
            "adm_country_filter_btn", 4
        )
        self.tmpl_vars['cr']['js'] += filters_js
        self.tmpl_vars['lc']['list_qs'] = self.manage_list_query_string(order_by, order_prog, filter_arr)
        
        self.tmpl_vars['lc']["adm_countryTab"]['filtered'] = False
        if len(filter_arr) > 0:
            self.tmpl_vars['lc']["adm_countryTab"]['filtered'] = True
        order = []
        self.tmpl_vars['lc']["adm_countryTab"]['rowsNum'] = self.adm_countryMd.select(True, ext_refs, quick_list,
            conds, [], None, 0, {})['data'][0]
        if self.tmpl_vars['lc']["adm_countryTab"]['rowsNum'] < 1:
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
                self.tmpl_vars['lc']["adm_countryTab"]['rowsNum'], ROWS_PER_PAGE, par_page, '', pag_pars, 'U')
            if par_page < 1 or par_page > self.paginator.pages_num:
                template_name = "_alerts/page_error"
            else:
                order = [["code", "ASC"]]
                if order_by != "":
                    order = [[order_by, order_prog]]  
                offset = (par_page - 1) * ROWS_PER_PAGE
                self.tmpl_vars['lc']["adm_countryTab"]['data'] = self.adm_countryMd.select(False,
                    ext_refs, quick_list, conds, order, limit, offset, {})['data']
                if len(self.tmpl_vars['lc']["adm_countryTab"]['data']) > 0:
                    self.tmpl_vars['lc']["adm_countryTab"]['hasData'] = True
                    self._manage_adm_country()

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def create(self, start_response):
        template_name = "adm_country/create"

        ext_refs = True
        quick_list = ["name", "code", "eu", "currency", "active"]
        not_required = ["eu", "active"]
        prefix = ''
        self.form.import_table(
            self.adm_countryMd.get_table_def(), self.tmpl_vars['lc']["adm_countryTab"]['T'],
            ext_refs, quick_list, not_required, prefix
        )

        self.form.form_def['ui']['eu']['widget'] = 'input-checkbox'
        self.form.form_def['ui']['active']['widget'] = 'input-checkbox'

        display = [
            ["name", 6, "code", 6],
            ["currency", 6, "eu", 3, "active", 3],
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
            self.tmpl_vars['lc']["adm_countryTab"]['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["adm_countryTab"]['T'], 
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
            # eu
            if not "eu" in f_values or str(f_values["eu"]) != "1":
                f_values["eu"] = "0"
            # active
            if not "active" in f_values or str(f_values["active"]) != "1":
                f_values["active"] = "0"


            # Gestione None


            # Verifica opzioni

            # Verifica clausola unique
            wrong_fields = self.verify_uniques("C", None,
                self.adm_countryMd, self.tmpl_vars['lc']["adm_countryTab"],
                f_values, {},
                wrong_fields)

            if len(wrong_fields) == 0:
                ps = {
                    "name": f_values["name"],
                    "code": f_values["code"].upper(),
                    "eu": f_values["eu"],
                    "currency": f_values["currency"].upper(),
                    "active": f_values["active"],
                    "creator_rid": 1,
                    "creation_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")            
                }
                location = self.tmpl_vars['cr']['links']["adm_country_list"] + "/1"
                res = self.adm_countryMd.insert(ps)
                self.close_controller()
                if res['err'] == True:
                    self.tmpl_vars['cr']['db_msg'] = res['msg']
                    template_name = "_alerts/db_error"
                    self.close_controller()
                    return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
                else:
                    location = self.tmpl_vars['cr']['links']["adm_country_read"] + "/" + str(res['data'][0])
                    self.close_controller()
                    start_response('302 Found', [('Location', location)])
                    return []
            else:
                self.set_csrf_cookie(csrf_value)
                f_values['_csrf'] = csrf_value
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
                self.tmpl_vars['lc']["adm_countryTab"]['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["adm_countryTab"]['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
    
    #
    def read(self, start_response):
        template_name = "adm_country/read"
        
        ext_refs = False
        quick_list = []
        conds = [
            ['W', 'AND', self.adm_countryMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        res =  self.adm_countryMd.select(False, ext_refs, quick_list, conds, order, 1, 0, {})

        self.tmpl_vars['lc']["adm_countryTab"]['data'] = self.adm_countryMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        
        if len(self.tmpl_vars['lc']["adm_countryTab"]['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        # adm_country
        self.tmpl_vars['lc']["adm_countryTab"]['rendered'] = ""
        self.tmpl_vars['lc']["adm_countryTab"]['hasData'] = True
        f_key_links = {}
        fields_to_html_escape = []
        self._manage_adm_country()
        self.tmpl_vars['lc']["adm_countryTab"]['rendered'] = self.render.render_record(
            self.adm_countryMd.get_table_columns_keys(),
            self.adm_countryMd.get_table_fKeys(),
            self.tmpl_vars['lc']["adm_countryTab"]['T'], 
            self.tmpl_vars['lc']["adm_countryTab"]['_data'],
            ext_refs, f_key_links, quick_list, fields_to_html_escape, 1
        )

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def update(self, start_response):
        template_name = "adm_country/update"

        ext_refs = False
        quick_list = ["name", "code", "eu", "currency", "active"]
        not_required = ["eu", "active"]
        conds = [
            ['W', 'AND', self.adm_countryMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        self.tmpl_vars['lc']["adm_countryTab"]['data'] = self.adm_countryMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        if len(self.tmpl_vars['lc']["adm_countryTab"]['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
        
        record_data = self.tmpl_vars['lc']["adm_countryTab"]['data'][0]

        prefix = ''
        self.form.import_table(
            self.adm_countryMd.get_table_def(), self.tmpl_vars['lc']["adm_countryTab"]['T'],
            ext_refs, quick_list, not_required, prefix
        )

        self.form.form_def['ui']['eu']['widget'] = 'input-checkbox'
        self.form.form_def['ui']['active']['widget'] = 'input-checkbox'

        display = [
            ["name", 6, "code", 6],
            ["currency", 6, "eu", 3, "active", 3],
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
            wrong_fields = []
            use_defaults = False
            after_submit = False
            self.tmpl_vars['lc']["adm_countryTab"]['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["adm_countryTab"]['T'], 
                display, form_attrs, record_data, wrong_fields, use_defaults, before_form_closing, after_submit, 
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
            # eu
            if not "eu" in f_values or str(f_values["eu"]) != "1":
                f_values["eu"] = "0"
            # active
            if not "active" in f_values or str(f_values["active"]) != "1":
                f_values["active"] = "0"


            # Gestione None

            ps = {}
            for k in f_values:
                v = f_values[k]
                if str(v) != str(record_data[k]) or k in self.adm_countryMd.get_table_columnsInUniques():
                    ps[k] = f_values[k]

            # Verifica opzioni

            # Verifica clausola unique
            wrong_fields = self.verify_uniques("U", None,
                self.adm_countryMd, self.tmpl_vars['lc']["adm_countryTab"],
                f_values, record_data,
                wrong_fields)

            if len(wrong_fields) == 0:
                location = self.tmpl_vars['cr']['links']["adm_country_read"] + "/" + str(self.ctx['params']['rid'])
                if len(ps) > 0:
                    if "code" in ps:
                        ps['code'].upper()
                    if "currency" in ps:
                        ps['currency'].upper()
                    self.adm_countryMd.update(ps, conds)
                self.close_controller()
                start_response('302 Found', [('Location', location)])
                return []
            else:
                self.set_csrf_cookie(csrf_value)
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg']['ErrInForm']
                self.tmpl_vars['lc']["adm_countryTab"]['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["adm_countryTab"]['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def delete(self, start_response):
        template_name = "adm_country/delete"
        
        ext_refs = False
        quick_list = ["name"]
        conds = [
            ['W', 'AND', self.adm_countryMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        self.tmpl_vars['lc']["adm_countryTab"]['data'] = self.adm_countryMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        if len(self.tmpl_vars['lc']["adm_countryTab"]['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        self.tmpl_vars['lc']["adm_countryTab"]['hasData'] = True
        f_key_links = {}
        fields_to_html_escape = []
        self.tmpl_vars['lc']["adm_countryTab"]['rendered'] = self.render.render_record(
            self.adm_countryMd.get_table_columns_keys(),
            self.adm_countryMd.get_table_fKeys(),
            self.tmpl_vars['lc']["adm_countryTab"]['T'], 
            self.tmpl_vars['lc']["adm_countryTab"]['data'],
            ext_refs, f_key_links, quick_list, fields_to_html_escape, 1
        )

        prefix = ''
        self.form.form_def = {
            "name": "",
            "prefix": prefix,
            "required": [],
            "dontValidate": [],
            "fields": {},
            "ui": {}
        }
        self.form.add_csrf_field()

        display = [
            ["name", 6, "code", 6],
            ["currency", 6, "eu", 3, "active", 3],
            ["_csrf", None]
        ]

        record_data = {}
        form_attrs = {"method": 'post', "novalidate": None}
        before_form_closing = ''
        csrf_value = self.generate_csrf_token()
        self.form.form_def['ui']['_csrf']['attrs']['value'] = csrf_value

        if self.tmpl_vars['env']['METHOD'] == 'GET':
            # GET
            self.tmpl_vars['cr']['method_GET'] = True
            self.set_csrf_cookie(csrf_value)
            wrong_fields = []
            use_defaults = False
            after_submit = False
            self.tmpl_vars['lc']["adm_countryTab"]['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["adm_countryTab"]['T'], 
                display, form_attrs, record_data, wrong_fields, use_defaults, before_form_closing, after_submit, 
                "", self.tmpl_vars['cr']['T']['btn_Delete']
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
            
            if len(wrong_fields) == 0:
                location = self.tmpl_vars['cr']['links']["adm_country_list"] + "/1"
                self.adm_countryMd.delete(conds)
                self.close_controller()
                start_response('302 Found', [('Location', location)])
                return []
            else:
                self.set_csrf_cookie(csrf_value)
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
                self.tmpl_vars['lc']["adm_countryTab"]['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["adm_countryTab"]['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def _manage_adm_country(self):
        self.tmpl_vars['lc']["adm_countryTab"]['_data'] = []
        if len(self.tmpl_vars['lc']["adm_countryTab"]['data']) > 0:
            keys = list(self.tmpl_vars['lc']["adm_countryTab"]['data'][0].keys())
            c = 0
            for row in self.tmpl_vars['lc']["adm_countryTab"]['data']:
                self.tmpl_vars['lc']["adm_countryTab"]['_data'].append({})
                for key in keys:
                    if key == "eu":
                        if str(row[key]) == "1":
                            self.tmpl_vars['lc']['adm_countryTab']['_data'][c][key] = '<span class="oi oi-check"></span>'
                        else:
                            self.tmpl_vars['lc']['adm_countryTab']['_data'][c][key] = ""
                    elif key == "active":
                        if str(row[key]) == "1":
                            self.tmpl_vars['lc']['adm_countryTab']['_data'][c][key] = '<span class="oi oi-check"></span>'
                        else:
                            self.tmpl_vars['lc']['adm_countryTab']['_data'][c][key] = ""
                    else:
                        self.tmpl_vars['lc']["adm_countryTab"]['_data'][c][key] = row[key]
                c += 1
        