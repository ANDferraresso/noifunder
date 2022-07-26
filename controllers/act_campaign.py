from datetime import datetime
import json
import core.controller as ctr
import core.form
import core.render
import core.paginator
import models.db.act_campaign
import models.tables.act_campaign
import models.db.act_project
import models.tables.act_project

ROWS_PER_PAGE = 50

#
class Act_Campaign(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)

        # act_campaign
        f = open("dictios/tables/act_campaign" + "_" + self.tmpl_vars['cr']['lang'] + ".json", "r")
        self.tmpl_vars['lc']['act_campaignTab'] = {
            "T": json.loads(f.read()),
            "data": [],
            "hasData": False
        }
        f.close()
        self.act_campaignMd = models.db.act_campaign.Act_Campaign(
            "sqlite", sqlite_conn,
            models.tables.act_campaign.items, "")

        # act_project
        f = open("dictios/tables/act_project" + "_" + self.tmpl_vars['cr']['lang'] + ".json", "r")
        self.tmpl_vars['lc']['act_projectTab'] = {
            "T": json.loads(f.read()),
            "data": [],
            "hasData": False
        }
        f.close()
        self.act_projectMd = models.db.act_project.Act_Project(
            "sqlite", sqlite_conn,
            models.tables.act_project.items, "")

        self.form = core.form.Form(self.ctx)
        self.render = core.render.Render()
        self.paginator = core.paginator.Paginator(self.ctx)

    #
    def list_all(self, start_response):
        template_name = "act_campaign/list"
        par_page = int(self.ctx['params']['page'])

        order_by, order_prog, self.tmpl_vars['lc']['order_prog'] = self.manage_list_order([
            "rid", "code", "title", "status", "start_date", "deadline"
        ])

        ext_refs = True
        quick_list = ["rid", "project_rid", "code", "title", "status", "start_date", "deadline"]
        conds = []
        limit = ROWS_PER_PAGE
        offset = 0

        # Filtri
        options = {
            "status": self.tmpl_vars['lc']['act_campaignTab']['T']['opts']['status'],
        }
        conds, filter_arr, filters_js, self.tmpl_vars['lc']['filterHTML'] = self.paginator.manage_filter(
            "sqlite", self.act_campaignMd, 
            ext_refs, quick_list, conds, options,
            self.tmpl_vars['cr']['links']['act_campaign_list'] + "/1" + "?", 
            "act_campaign_filter_btn", 4
        )
        self.tmpl_vars['cr']['js'] += filters_js
        self.tmpl_vars['lc']['list_qs'] = self.manage_list_query_string(order_by, order_prog, filter_arr)
        
        self.tmpl_vars['lc']['act_campaignTab']['filtered'] = False
        if len(filter_arr) > 0:
            self.tmpl_vars['lc']['act_campaignTab']['filtered'] = True
        order = []
        self.tmpl_vars['lc']['act_campaignTab']['rowsNum'] = self.act_campaignMd.select(True, ext_refs, quick_list,
            conds, [], None, 0, {})['data'][0]

        if self.tmpl_vars['lc']['act_campaignTab']['rowsNum'] < 1:
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
                self.tmpl_vars['lc']['act_campaignTab']['rowsNum'], ROWS_PER_PAGE, par_page, '', pag_pars, 'U')
            if par_page < 1 or par_page > self.paginator.pages_num:
                template_name = "_alerts/page_error"
            else:
                order = [["code", "ASC"]]
                if order_by != "":
                    order = [[order_by, order_prog]]  
                offset = (par_page - 1) * ROWS_PER_PAGE
                self.tmpl_vars['lc']['act_campaignTab']['data'] = self.act_campaignMd.select(False,
                    ext_refs, quick_list, conds, order, limit, offset, {})['data']
                if len(self.tmpl_vars['lc']['act_campaignTab']['data']) > 0:
                    self.tmpl_vars['lc']['act_campaignTab']['hasData'] = True
                    self._manage_act_campaign()

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def create(self, start_response):
        template_name = "act_campaign/create"

        ext_refs = True
        quick_list = ["project_rid", "code", "title", "start_date", "deadline", "memo"]
        not_required = []
        prefix = ''
        self.form.import_table(
            self.act_campaignMd.get_table_def(), self.tmpl_vars['lc']['act_campaignTab']['T'],
            ext_refs, quick_list, not_required, prefix
        )

        # project_rid
        self.form.form_def['ui']['project_rid']['widget'] = 'select'
        # start_date
        self.form.form_def['ui']['start_date']['widget'] = 'input-date'
        # deadline
        self.form.form_def['ui']['deadline']['widget'] = 'input-date'
        # memo
        self.form.form_def['ui']['memo']['widget'] = 'textarea'
        self.form.form_def['ui']['memo']['attrs']['rows'] = 3

        # Carica opzioni 
        # project_rid
        self.form.form_def['ui']['project_rid']['options'] = self.act_projectMd.get_options([], False)['data']

        display = [
            ["project_rid", 12], 
            ["code", 4, "title", 8], 
            ["start_date", 6, "deadline", 6], 
            ["memo", 12], 
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
            self.tmpl_vars['lc']['act_campaignTab']['renderedForm'], js = self.render.render_form(
                self.form.form_def,
                self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']['act_campaignTab']['T'], 
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
            # project_rid
            key = "project_rid"
            if key in f_values and not key in wrong_fields and not key in self.form.form_def['dontValidate']:
                if not self.check_option(f_values[key], self.form.form_def['ui'][key]['options']):
                    if not key in wrong_fields:
                        wrong_fields.append(key)
                    self.tmpl_vars['lc']['act_campaignTab']['T']['msg'][key] += " " + self.tmpl_vars['cr']['T']['msg_ErrExtKey']
            # status
            key = "status"
            if key in f_values and not key in wrong_fields and not key in self.form.form_def['dontValidate']:
                if not self.check_option(f_values[key], self.form.form_def['ui'][key]['options']):
                    if not key in wrong_fields:
                        wrong_fields.append(key)
                    self.tmpl_vars['lc']['act_campaignTab']['T']['msg'][key] += " " + self.tmpl_vars['cr']['T']['msg_ErrExtKey']

            # Verifica clausola unique
            wrong_fields = self.verify_uniques("C", None,
                self.act_campaignMd, self.tmpl_vars['lc']['act_campaignTab'],
                f_values, {},
                wrong_fields)

            if len(wrong_fields) == 0:
                ps = {
                    "project_rid": f_values['project_rid'], 
                    "code": f_values['code'].upper(), 
                    "title": f_values['title'], 
                    "status": "O", 
                    "start_date": f_values['start_date'], 
                    "deadline": f_values['deadline'], 
                    "memo": f_values['memo'],
                    "creator_rid": 1, 
                    "creation_dt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    
                }
                location = self.tmpl_vars['cr']['links']['act_campaign_list'] + "/1"
                res = self.act_campaignMd.insert(ps)
                self.close_controller()
                if res['err'] == True:
                    self.tmpl_vars['cr']['db_msg'] = res['msg']
                    template_name = "_alerts/db_error"
                    self.close_controller()
                    return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
                else:
                    location = self.tmpl_vars['cr']['links']['act_campaign_read'] + "/" + str(res['data'][0])
                    self.close_controller()
                    start_response('302 Found', [('Location', location)])
                    return []
            else:
                self.set_csrf_cookie(csrf_value)
                f_values['_csrf'] = csrf_value
                use_defaults = False
                after_submit = True
                self.tmpl_vars['lc']['alert'] = self.tmpl_vars['cr']['T']['msg_ErrInForm']
                self.tmpl_vars['lc']['act_campaignTab']['renderedForm'], js = self.render.render_form(
                    self.form.form_def,
                    self.tmpl_vars['cr']['T'], self.tmpl_vars['lc']['act_campaignTab']['T'], 
                    display, form_attrs, f_values, wrong_fields, use_defaults, before_form_closing, after_submit, 
                    "", self.tmpl_vars['cr']['T']['btn_Send']
                )
                self.tmpl_vars['cr']['js'] += js

                self.close_controller()
                return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)
    
    #
    def read(self, start_response):
        template_name = "act_campaign/read"
        
        ext_refs = True
        quick_list = []
        conds = [
            ['W', 'AND', self.act_campaignMd.get_table_name(), 'rid', '=', int(self.ctx['params']['rid']), '']
        ]
        order = []
        self.act_campaignMd.select(False, ext_refs, quick_list, conds, order, 1, 0, {})
        self.tmpl_vars['lc']['act_campaignTab']['data'] = self.act_campaignMd.select(False,
            ext_refs, quick_list, conds, order, 1, 0, {})['data']
        
        if len(self.tmpl_vars['lc']['act_campaignTab']['data']) == 0:
            template_name = "_alerts/no_resource_error"
            self.close_controller()
            return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

        self.tmpl_vars['lc']['act_campaignTab']['rendered'] = ""
        self.tmpl_vars['lc']['act_campaignTab']['hasData'] = True
        f_key_links = {
            "project_rid": self.tmpl_vars['cr']['links']['act_project_read']
        }
        fields_to_html_escape = []
        self._manage_act_campaign()
        self.tmpl_vars['lc']['act_campaignTab']['rendered'] = self.render.render_record(
            self.act_campaignMd.get_table_columns_keys(),
            self.act_campaignMd.get_table_fKeys(),
            self.tmpl_vars['lc']['act_campaignTab']['T'], 
            self.tmpl_vars['lc']['act_campaignTab']['_data'],
            ext_refs, f_key_links, quick_list, fields_to_html_escape, 1
        )

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def update(self, start_response):
        template_name = "act_campaign/update"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def delete(self, start_response):
        template_name = "act_campaign/delete"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def _manage_act_campaign(self):
        self.tmpl_vars['lc']['act_campaignTab']['_data'] = []
        if len(self.tmpl_vars['lc']['act_campaignTab']['data']) > 0:
            keys = list(self.tmpl_vars['lc']['act_campaignTab']['data'][0].keys())
            c = 0
            for row in self.tmpl_vars['lc']['act_campaignTab']['data']:
                self.tmpl_vars['lc']['act_campaignTab']['_data'].append({})
                for key in keys:
                    if key == "status":
                        self.tmpl_vars['lc']['act_campaignTab']['_data'][c][key] = self.get_option(
                            str(row[key]), self.tmpl_vars['lc']['act_campaignTab']['T']['opts'][key])
                    else:
                        self.tmpl_vars['lc']['act_campaignTab']['_data'][c][key] = row[key]
                c += 1