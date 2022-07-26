from datetime import datetime
import json
import core.controller as ctr
import core.form
import core.render
import core.paginator
import models.db.acc_gift
import models.tables.acc_gift

ROWS_PER_PAGE = 50

#
class Acc_Gift(ctr.Controller):
    #
    def __init__(self, sqlite_conn, ctx, tmpl_vars, url_t):
        super().__init__(sqlite_conn, ctx, tmpl_vars, url_t)

        # acc_gift
        f = open("dictios/tables/acc_gift" + "_" + self.tmpl_vars['cr']['lang'] + ".json", "r")
        self.tmpl_vars['lc']['acc_giftTab'] = {
            "T": json.loads(f.read()),
            "data": [],
            "hasData": False
        }
        f.close()
        self.acc_giftMd = models.db.acc_gift.Act_Project(
            "sqlite", sqlite_conn,
            models.tables.acc_gift.items, "")

        self.form = core.form.Form(self.ctx)
        self.render = core.render.Render()
        self.paginator = core.paginator.Paginator(self.ctx)

    #
    def list_all(self, start_response):
        template_name = "acc_gift/list"
        par_page = int(self.ctx['params']['page'])

        order_by, order_prog, self.tmpl_vars['lc']['order_prog'] = self.manage_list_order([
            "rid", "code", "title", "status", "start_date", "deadline"
        ])

        ext_refs = False
        quick_list = ["rid", "code", "title", "status", "start_date", "deadline"]
        conds = []
        limit = ROWS_PER_PAGE
        offset = 0

        # Filtri
        options = {
            "status": self.tmpl_vars['lc']['acc_giftTab']['T']['opts']['status'],
        }
        conds, filter_arr, filters_js, self.tmpl_vars['lc']['filterHTML'] = self.paginator.manage_filter(
            "sqlite", self.acc_giftMd, 
            ext_refs, quick_list, conds, options,
            self.tmpl_vars['cr']['links']['acc_gift_list'] + "/1" + "?", 
            "acc_gift_filter_btn", 4
        )
        self.tmpl_vars['cr']['js'] += filters_js
        self.tmpl_vars['lc']['list_qs'] = self.manage_list_query_string(order_by, order_prog, filter_arr)
        
        self.tmpl_vars['lc']['acc_giftTab']['filtered'] = False
        if len(filter_arr) > 0:
            self.tmpl_vars['lc']['acc_giftTab']['filtered'] = True
        order = []
        self.tmpl_vars['lc']['acc_giftTab']['rowsNum'] = self.acc_giftMd.select(True, ext_refs, quick_list,
            conds, [], None, 0, {})['data'][0]
        if self.tmpl_vars['lc']['acc_giftTab']['rowsNum'] < 1:
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
                self.tmpl_vars['lc']['acc_giftTab']['rowsNum'], ROWS_PER_PAGE, par_page, '', pag_pars, 'U')
            if par_page < 1 or par_page > self.paginator.pages_num:
                template_name = "_alerts/page_error"
            else:
                order = [["code", "ASC"]]
                if order_by != "":
                    order = [[order_by, order_prog]]  
                offset = (par_page - 1) * ROWS_PER_PAGE
                self.tmpl_vars['lc']['acc_giftTab']['data'] = self.acc_giftMd.select(False,
                    ext_refs, quick_list, conds, order, limit, offset, {})['data']
                if len(self.tmpl_vars['lc']['acc_giftTab']['data']) > 0:
                    self.tmpl_vars['lc']['acc_giftTab']['hasData'] = True
                    self._manage_acc_gift()

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def create(self, start_response):
        template_name = "acc_gift/create"

        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def read(self, start_response):
        template_name = "acc_gift/read"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def update(self, start_response):
        template_name = "acc_gift/update"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)

    #
    def delete(self, start_response):
        template_name = "acc_gift/delete"
        
        self.close_controller()
        return self.tmpl.render_page(start_response, template_name, self.tmpl_vars, "", [], self.cookies)