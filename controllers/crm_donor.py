from datetime import datetime
import json
import core.controller as ctr
import core.form
import core.render
import core.paginator
import models.db.crm_donor
import models.tables.crm_donor

ROWS_PER_PAGE = 50

#
class Crm_Donor(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)

        # crm_donor
        f = open("dictios/tables/crm_donor" + "_" + self.tmpl_vars["cr"]["lang"] + ".json", "r")
        self.tmpl_vars["lc"]["crm_donorTab"] = {
            "T": json.loads(f.read()),
            "data": [],
            "hasData": False
        }
        f.close()
        self.crm_donorMd = models.db.crm_donor.Crm_Donor(
            "sqlite", sqlite_conn,
            models.tables.crm_donor.items, "")

        self.form = core.form.Form(self.ctx)
        self.render = core.render.Render()
        self.paginator = core.paginator.Paginator(self.ctx)        

    #
    def list_all(self, start_response):
        template_name = "crm_donor/list"
        par_page = int(self.ctx['params']['page'])

        order_by, order_prog, self.tmpl_vars['lc']['order_prog'] = self.manage_list_order([
            "rid", "donor_type", "name", "first_name", "last_name", "business_name", "birth_date", "sex", "tax_code", "vat_number", "country_rid", "city", "zip_code", "address_row_1", "address_row_2", "creation_dt", "creator_rid"
        ])

        ext_refs = False
        quick_list = ["rid", "donor_type", "name", "first_name", "last_name", "business_name", "birth_date", "sex", "tax_code", "vat_number", "country_rid", "city", "zip_code", "address_row_1", "address_row_2", "creation_dt", "creator_rid"]
        conds = []
        limit = ROWS_PER_PAGE
        offset = 0

        # Filtri
        options = {
        }
        conds, filter_arr, filters_js, self.tmpl_vars['lc']['filterHTML'] = self.paginator.manage_filter(
            "sqlite", self.crm_donorMd, 
            ext_refs, quick_list, conds, options,
            self.tmpl_vars['cr']['links']["crm_donor_list"] + "/1" + "?", 
            "crm_donor_filter_btn", 4
        )
        self.tmpl_vars['cr']['js'] += filters_js
        self.tmpl_vars['lc']['list_qs'] = self.manage_list_query_string(order_by, order_prog, filter_arr)
        
        self.tmpl_vars['lc']["crm_donorTab"]['filtered'] = False
        if len(filter_arr) > 0:
            self.tmpl_vars['lc']["crm_donorTab"]['filtered'] = True
        order = []
        self.tmpl_vars['lc']["crm_donorTab"]['rowsNum'] = self.crm_donorMd.select(True, ext_refs, quick_list,
            conds, [], None, 0, {})['data'][0]
        if self.tmpl_vars['lc']["crm_donorTab"]['rowsNum'] < 1:
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
                self.tmpl_vars['lc']["crm_donorTab"]['rowsNum'], ROWS_PER_PAGE, par_page, '', pag_pars, 'U')
            if par_page < 1 or par_page > self.paginator.pages_num:
                template_name = "_alerts/page_error"
            else:
                order = [["code", "ASC"]]
                if order_by != "":
                    order = [[order_by, order_prog]]  
                offset = (par_page - 1) * ROWS_PER_PAGE
                self.tmpl_vars['lc']["crm_donorTab"]['data'] = self.crm_donorMd.select(False,
                    ext_refs, quick_list, conds, order, limit, offset, {})['data']
                if len(self.tmpl_vars['lc']["crm_donorTab"]['data']) > 0:
                    self.tmpl_vars['lc']["crm_donorTab"]['hasData'] = True
                    self._manage_crm_donor()

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def create(self, start_response):
        template_name = "crm_donor/create"

        ext_refs = True
        quick_list = ["donor_type", "name", "first_name", "last_name", "business_name", "birth_date", "sex", "tax_code", "vat_number", "country_rid", "city", "zip_code", "address_row_1", "address_row_2", "creation_dt", "creator_rid"]
        not_required = []
        prefix = ''
        self.form.import_table(
            self.crm_donorMd.get_table_def(), self.tmpl_vars['lc']["crm_donorTab"]['T'],
            ext_refs, quick_list, not_required, prefix
        )

        # birth_date
        self.form.form_def['ui']['birth_date']['widget'] = 'input-date'


        display = [
            ["donor_type", 12],
            ["name", 12],
            ["first_name", 12],
            ["last_name", 12],
            ["business_name", 12],
            ["birth_date", 12],
            ["sex", 12],
            ["tax_code", 12],
            ["vat_number", 12],
            ["country_rid", 12],
            ["city", 12],
            ["zip_code", 12],
            ["address_row_1", 12],
            ["address_row_2", 12],
            ["creation_dt", 12],
            ["creator_rid", 12],
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
            self.tmpl_vars['lc']["crm_donorTab"]['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["crm_donorTab"]['T'], 
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
            # status
            key = "status"
            if key in f_values and not key in wrong_fields and not key in self.form.form_def['dontValidate']:
                if not self.check_option(f_values[key], self.form.form_def['ui'][key]['options']):
                    if not key in wrong_fields:
                        wrong_fields.append(key)
                    self.tmpl_vars['lc']["crm_donorTab"]['T']['msg'][key] += " " + self.tmpl_vars['cr']['T']['msg_ErrExtKey']

            # Verifica clausola unique
            wrong_fields = self.verify_uniques("C", None,
                self.crm_donorMd, self.tmpl_vars['lc']["crm_donorTab"],
                f_values, {},
                wrong_fields)

            if len(wrong_fields) == 0:
                ps = {
                    "donor_type": f_values["donor_type"],
                    "name": f_values["name"],
                    "first_name": f_values["first_name"],
                    "last_name": f_values["last_name"],
                    "business_name": f_values["business_name"],
                    "birth_date": f_values["birth_date"],
                    "sex": f_values["sex"],
                    "tax_code": f_values["tax_code"],
                    "vat_number": f_values["vat_number"],
                    "country_rid": f_values["country_rid"],
                    "city": f_values["city"],
                    "zip_code": f_values["zip_code"],
                    "address_row_1": f_values["address_row_1"],
                    "address_row_2": f_values["address_row_2"],
                    "creation_dt": f_values["creation_dt"],
                    "creator_rid": f_values["creator_rid"],
                    "creator_rid": 1,
                    "creation_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")            
                }
                location = self.tmpl_vars['cr']['links']["crm_donor_list"] + "/1"
                res = self.crm_donorMd.insert(ps)
                self.close_controller()
                if res['err'] == True:
                    self.tmpl_vars['cr']['db_msg'] = res['msg']
                    template_name = "_alerts/db_error"
                    self.close_controller()
                    return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
                else:
                    location = self.tmpl_vars['cr']['links']["crm_donor_read"] + "/" + str(res['data'][0])
                    self.close_controller()
                    start_response('302 Found', [('Location', location)])
                    return []
            else:
                self.set_csrf_cookie(csrf_value)
                f_values['_csrf'] = csrf_value
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
                self.tmpl_vars['lc']["crm_donorTab"]['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["crm_donorTab"]['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
    
    #
    def read(self, start_response):
        template_name = "crm_donor/read"
        
        ext_refs = False
        quick_list = []
        conds = [
            ['W', 'AND', self.crm_donorMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        res =  self.crm_donorMd.select(False, ext_refs, quick_list, conds, order, 1, 0, {})
        print(res)
        self.tmpl_vars['lc']["crm_donorTab"]['data'] = self.crm_donorMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        
        if len(self.tmpl_vars['lc']["crm_donorTab"]['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        # crm_donor
        self.tmpl_vars['lc']["crm_donorTab"]['rendered'] = ""
        self.tmpl_vars['lc']["crm_donorTab"]['hasData'] = True
        f_key_links = {}
        fields_to_html_escape = []
        self._manage_crm_donor()
        self.tmpl_vars['lc']["crm_donorTab"]['rendered'] = self.render.render_record(
            self.crm_donorMd.get_table_columns_keys(),
            self.crm_donorMd.get_table_fKeys(),
            self.tmpl_vars['lc']["crm_donorTab"]['T'], 
            self.tmpl_vars['lc']["crm_donorTab"]['_data'],
            ext_refs, f_key_links, quick_list, fields_to_html_escape, 1
        )

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def update(self, start_response):
        template_name = "crm_donor/update"

        ext_refs = False
        quick_list = ["donor_type", "name", "first_name", "last_name", "business_name", "birth_date", "sex", "tax_code", "vat_number", "country_rid", "city", "zip_code", "address_row_1", "address_row_2", "creation_dt", "creator_rid"]
        not_required = ["qlink"]
        conds = [
            ['W', 'AND', self.crm_donorMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        self.tmpl_vars['lc']["crm_donorTab"]['data'] = self.crm_donorMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        if len(self.tmpl_vars['lc']["crm_donorTab"]['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
        
        record_data = self.tmpl_vars['lc']["crm_donorTab"]['data'][0]

        prefix = ''
        self.form.import_table(
            self.crm_donorMd.get_table_def(), self.tmpl_vars['lc']["crm_donorTab"]['T'],
            ext_refs, quick_list, not_required, prefix
        )

        # birth_date
        self.form.form_def['ui']['birth_date']['widget'] = 'input-date'


        # Carica opzioni 
        # str_controller_rid
        self.form.form_def['ui']['str_controller_rid']['options'] = self.str_controllerMd.get_options([], False)['data']

        display = [
            ["donor_type", 12],
            ["name", 12],
            ["first_name", 12],
            ["last_name", 12],
            ["business_name", 12],
            ["birth_date", 12],
            ["sex", 12],
            ["tax_code", 12],
            ["vat_number", 12],
            ["country_rid", 12],
            ["city", 12],
            ["zip_code", 12],
            ["address_row_1", 12],
            ["address_row_2", 12],
            ["creation_dt", 12],
            ["creator_rid", 12],
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
            self.tmpl_vars['lc']["crm_donorTab"]['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["crm_donorTab"]['T'], 
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
            # qlink
            if not "qlink" in f_values or str(f_values['qlink']) != "1":
                f_values['qlink'] = "0"

            # Gestione None
            # ...

            ps = {}
            for k in f_values:
                v = f_values[k]
                if str(v) != str(record_data[k]) or k in self.adm_countryMd.get_table_columnsInUniques():
                    ps[k] = f_values[k]

            # Verifica opzioni
            # method
            key = "method"
            if key in ps and not key in wrong_fields and not key in self.form.form_def['dontValidate']:
                if not self.check_option(ps[key], self.form.form_def['ui'][key]['options']):
                    if not key in wrong_fields:
                        wrong_fields.append(key)
                    self.tmpl_vars['lc']["crm_donorTab"]['T']['msg'][key] += " " + self.tmpl_vars['cr']['T']['msg_ErrExtKey']
            # str_controller_rid
            key = "str_controller_rid"
            if key in ps and not key in wrong_fields and not key in self.form.form_def['dontValidate']:
                if not self.check_option(ps[key], self.form.form_def['ui'][key]['options']):
                    if not key in wrong_fields:
                        wrong_fields.append(key)
                    self.tmpl_vars['lc']["crm_donorTab"]['T']['msg'][key] += " " + self.tmpl_vars['cr']['T']['msg_ErrExtKey']

            # Verifica clausola unique
            wrong_fields = self.verify_uniques("U", None,
                self.crm_donorMd, self.tmpl_vars['lc']["crm_donorTab"],
                f_values, record_data,
                wrong_fields)

            if len(wrong_fields) == 0:
                location = self.tmpl_vars['cr']['links']["crm_donor_read"] + "/" + str(self.ctx['params']['rid'])
                if len(ps) > 0:
                    ressss = self.crm_donorMd.update(ps, conds)
                    print(ressss)
                self.close_controller()
                start_response('302 Found', [('Location', location)])
                return []
            else:
                self.set_csrf_cookie(csrf_value)
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg']['ErrInForm']
                self.tmpl_vars['lc']["crm_donorTab"]['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["crm_donorTab"]['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def delete(self, start_response):
        template_name = "crm_donor/delete"
        
        ext_refs = False
        quick_list = ["name"]
        conds = [
            ['W', 'AND', self.crm_donorMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        self.tmpl_vars['lc']["crm_donorTab"]['data'] = self.crm_donorMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        if len(self.tmpl_vars['lc']["crm_donorTab"]['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        self.tmpl_vars['lc']["crm_donorTab"]['hasData'] = True
        f_key_links = {}
        fields_to_html_escape = []
        self.tmpl_vars['lc']["crm_donorTab"]['rendered'] = self.render.render_record(
            self.crm_donorMd.get_table_columns_keys(),
            self.crm_donorMd.get_table_fKeys(),
            self.tmpl_vars['lc']["crm_donorTab"]['T'], 
            self.tmpl_vars['lc']["crm_donorTab"]['data'],
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
            self.tmpl_vars['lc']["crm_donorTab"]['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["crm_donorTab"]['T'], 
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
                location = self.tmpl_vars['cr']['links']["crm_donor_list"] + "/1"
                self.crm_donorMd.delete(conds)
                self.close_controller()
                start_response('302 Found', [('Location', location)])
                return []
            else:
                self.set_csrf_cookie(csrf_value)
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
                self.tmpl_vars['lc']["crm_donorTab"]['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']["crm_donorTab"]['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def _manage_crm_donor(self):
        self.tmpl_vars['lc']["crm_donorTab"]['_data'] = []
        if len(self.tmpl_vars['lc']["crm_donorTab"]['data']) > 0:
            keys = list(self.tmpl_vars['lc']["crm_donorTab"]['data'][0].keys())
            c = 0
            for row in self.tmpl_vars['lc']["crm_donorTab"]['data']:
                self.tmpl_vars['lc']["crm_donorTab"]['_data'].append({})
                for key in keys:
                    if key == "status":
                        pass
                        # self.tmpl_vars['lc']["crm_donorTab"]['_data'][c][key] = self.get_option(
                        #     str(row[key]), self.tmpl_vars['lc']["crm_donorTab"]['T']['opts'][key])
                    else:
                        self.tmpl_vars['lc']["crm_donorTab"]['_data'][c][key] = row[key]
                c += 1