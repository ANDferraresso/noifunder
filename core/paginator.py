import math

#
class Paginator:
    #
    def __init__(self, ctx):
        self.ctx = ctx
        self.pages_num = 0
        self.page = 0
        self.first_page = 0
        self.prev_page = 0
        self.next_page = 0
        self.last_page = 0

    #
    def _calc(self, rows_num, row_per_page, page):
        if rows_num == 0:
            self.pages_num = 0
            self.page = 0
            self.first_page = 0
            self.prev_page = 0
            self.next_page = 0
            self.last_page = 0
        
        self.pages_num = math.floor(rows_num / row_per_page)
        if rows_num % row_per_page > 0: 
            self.pages_num += 1

        self.page = page
        if self.page < 1 or self.page > self.pages_num: 
            self.page = 1

        self.first_page = 1
        self.last_page = self.pages_num; 

        self.prev_page = self.page - 1
        if self.prev_page < 1:
            self.prev_page = 1

        self.next_page = self.page + 1
        if self.next_page > self.last_page: 
            self.next_page = self.last_page

        return

    #
    def manage_filter(self, db_engine, model, ext_refs, quick_list, list_all_conds, 
        options, list_url, btn_name, colspan):
        conds = list_all_conds
        filter_html = ""
        filter_js = ""

        table_def = model.get_table_def()

        cls_keys = list(table_def['columns'].keys())
        columns = []
        if len(quick_list) > 0: 
            columns = quick_list
        else: 
            for v in cls_keys:
                columns.append(v)

        filter_list = {}
        filter_arr = {}

        if not ext_refs:
            # ext_refs = False
            # columns
            for v in columns:
                if 'filter_' + v in self.ctx['url_parts']['query'] \
                    and self.ctx['url_parts']['query']['filter_' + v] != "":
                    #
                    t = self.ctx['url_parts']['query']['filter_' + v]
                    t = t[0:30]
                    filter_list[v] = t
                    filter_arr['filter_' + v] = t
            # conds
            for k in filter_list:
                v = filter_list[k]
                v = str(v); 
                if v != "":
                    conds.append( ['W', 'AND', model.get_table_name(), k, 'LIKE', '%' + v + '%', ''] )
            # HTML
            filter_html = ""
            for v in columns:
                if v in options:
                    filter_html += "\n" + '      <th scope="col"><select class="form-select form-select-sm name="filter_' + v + '" id="filter_' + v + '_id">'
                    filter_html += '<option value=""></option>'
                    for elem in options[v]:
                        optK = list(elem.keys())[0]
                        optV = elem[optK]
                        if "filter_" + v in filter_arr and filter_arr['filter_' + v] == optK:
                            filter_html += '<option value="' + optK + '" selected="selected">' + optV + '</option>'
                        else:
                            filter_html += '<option value="' + optK + '">' + optV + '</option>'
                    filter_html += '</select></th>' + "\n"
                else:
                    if "filter_" + v in filter_arr:
                        filter_html += '      <th scope="col"><input type="text" maxlength="30" class="form-control form-control-sm" name="filter_' + v + '" id="filter_' + v + '_id" value="' + str(filter_arr["filter_" + v]) + '" /></th>' + "\n"
                    else:
                        filter_html += '      <th scope="col"><input type="text" maxlength="30" class="form-control form-control-sm" name="filter_' + v + '" id="filter_' + v + '_id" /></th>' + "\n"
            filter_html += '      <th scope="col" colspan="' + str(colspan) + '"><button type="button" id="' + btn_name + '" class="btn btn-secondary btn-sm">Filtra</button></th>' + "\n"
            # Js
            filter_js = "" \
                + "\n" + 'let btn = document.getElementById("' + btn_name + '");' \
                + "\n" + 'if (btn != null) {' \
                + '  btn.addEventListener("click", function (event) {' \
                + "\n" + '    event.preventDefault();' \
                + "\n" + '    let filters = {};' \
                + "\n" + '    let location = "' + list_url + '"'
            for v in columns:
                filter_js += "\n" + '    filters["' + v + '"] = String(document.getElementById("filter_' + v + '_id").value).substring(0, 30);'
            filter_js += "\n" + '    for (let key in filters) {' 
            filter_js += "\n" + '      if (filters[key] !== "") location += "filter_" + key + "=" + filters[key] + "&";' 
            filter_js += "\n" + '    }'
            filter_js += "\n" + '    if (location.charAt(location.length - 1) == "?") location = location.substring(0, location.length - 1);' 
            filter_js += "\n" + '    else if (location.charAt(location.length - 1) == "&") location = location.substring(0, location.length - 1);' 
            filter_js += "\n" + '    document.location.href = location;'
            filter_js += "\n" + '  });'
            filter_js += "\n" + '}'

        else:
            # ext_refs = TRUE
            # columns
            for v in columns:
                if v in table_def['fKeys']:
                    if 'filter_' + v + '_FK' in self.ctx['url_parts']['query'] \
                        and self.ctx['url_parts']['query']['filter_' + v + '_FK'] != "":
                        #
                        t = self.ctx['url_parts']['query']['filter_' + v + '_FK']
                        t = t[0:30]
                        filter_list[v + '_FK'] = t
                        filter_arr["filter_" + v + '_FK'] = t
                else:
                    if 'filter_' + v in self.ctx['url_parts']['query'] \
                        and self.ctx['url_parts']['query']['filter_' + v] != "":
                        #
                        t = self.ctx['url_parts']['query']['filter_' + v]
                        t = t[0:30]
                        filter_list[v] = t
                        filter_arr["filter_" + v] = t
            # conds
            for k in filter_list:
                v = filter_list[k]
                v = str(v)
                if k[-3:] == '_FK':
                    if v != "":
                        if db_engine == "sqlite":
                            conds.append( ['W', 'AND', '', k, 'LIKE', '%' + v + '%', ''] )
                        elif db_engine == "mysql":
                            conds.append( ['W', 'AND', '', k, 'LIKE', '%' + v + '%', ''] )
                    else:
                        pass
                else:
                    if v != "":
                        conds.append( ['W', 'AND', model.get_table_name(), k, 'LIKE', '%' + v + '%', ''] )
                    else:
                        pass

            # HTML
            filter_html = ""
            for v in columns:
                if v in options:
                    if v in table_def['fKeys']:
                        filter_html += "\n" + '      <th scope="col"><select class="form-select form-select-sm" name="filter_' + v + '_FK" id="filter_' + v + '_FK_id">'
                    else:
                        filter_html += "\n" + '      <th scope="col"><select class="form-select form-select-sm" name="filter_' + v + '" id="filter_' + v +'_id">'
                    filter_html += '<option value=""></option>'
                    for elem in options[v]:
                        optK = list(elem.keys())[0]
                        optV = elem[optK]
                        if v in table_def['fKeys']:
                            if "filter_" + v + "_FK" in filter_arr and filter_arr['filter_' + v + '_FK'] == optK:
                                filter_html += '<option value="' + optK + '" selected="selected">' + optV + '</option>'
                            else:
                                filter_html += '<option value="' + optK + '">' + optV + '</option>'
                        else:
                            if "filter_" + v in filter_arr and filter_arr['filter_' + v] == optK:
                                filter_html += '<option value="' + optK + '" selected="selected">' + optV + '</option>'
                            else:
                                filter_html += '<option value="' + optK + '">' + optV + '</option>'
                    filter_html += '</select></th>' + "\n"
                else:
                    if v in table_def['fKeys']:
                        if "filter_" + v + "_FK" in filter_arr:
                            filter_html += '      <th scope="col"><input type="text" maxlength="30" class="form-control form-control-sm" name="filter_' + v + '_FK" id="filter_' + v + '_FK_id" value="' + str(filter_arr["filter_" + v + "_FK"]) + '" /></th>' + "\n"
                        else:
                            filter_html += '      <th scope="col"><input type="text" maxlength="30" class="form-control form-control-sm" name="filter_' + v + '_FK" id="filter_' + v + '_FK_id" value="" /></th>' + "\n"
                    else:
                        if "filter_" + v in filter_arr:
                            filter_html += '      <th scope="col"><input type="text" maxlength="30" class="form-control form-control-sm" name="filter_' + v + '" id="filter_' + v + '_id" value="' + str(filter_arr["filter_" + v]) + '" /></th>' + "\n"
                        else:
                            filter_html += '      <th scope="col"><input type="text" maxlength="30" class="form-control form-control-sm" name="filter_' + v + '" id="filter_' + v + '_id" value="" /></th>' + "\n"

            filter_html += '      <th scope="col" colspan="' + str(colspan) + '"><button type="button" id="' + btn_name + '" class="btn btn-secondary btn-sm">Filtra</button></th>' + "\n"
            # Js
            filter_js = "" \
                + "\n" + 'let btn = document.getElementById("' + btn_name + '");' \
                + "\n" + 'if (btn != null) {' \
                + '  btn.addEventListener("click", function (event) {' \
                + "\n" + '    event.preventDefault();' \
                + "\n" + '    let filters = {};' \
                + "\n" + '    let location = "' + list_url + '"'
            for v in columns:
                if v in table_def['fKeys']:
                    if v in options:
                        filter_js += "\n" + '    filters["' + v + '_FK"] = String(document.getElementById("filter_' + v + '_FK_id").value).substring(0, 30);'
                    else:
                        filter_js += "\n" + '    filters["' + v + '_FK"] = String(document.getElementById("filter_' + v + '_FK_id").value).substring(0, 30);'
                else:
                    filter_js += "\n" + '    filters["' + v + '"] = String(document.getElementById("filter_' + v + '_id").value).substring(0, 30);'
            filter_js += "\n" + '    for (let key in filters) {' 
            filter_js += "\n" + '      if (filters[key] !== "") location += "filter_" + key + "=" + filters[key] + "&";' 
            filter_js += "\n" + '    }'
            filter_js += "\n" + '    if (location.charAt(location.length - 1) == "?") location = location.substring(0, location.length - 1);' 
            filter_js += "\n" + '    else if (location.charAt(location.length - 1) == "&") location = location.substring(0, location.length - 1);' 
            filter_js += "\n" + '    document.location.href = location;'
            filter_js += "\n" + '  });'
            filter_js += "\n" + '}'
    
        return conds, filter_arr, filter_js, filter_html

    #
    def pag_html(self, rows_num, row_per_page, page, link, pars, show_page_mode):
        self._calc(rows_num, row_per_page, page)
        queries = "?"
        for k in pars:
            v = pars[k]
            queries += k + "=" + v + "&"
        queries = queries.rstrip("&")
        if queries == "?":
            queries = ""

        html = '<nav aria-label=""><ul class="pagination">'

        if self.first_page != self.prev_page:
            if show_page_mode == "U":
                html += '<li class="page-item" id="pag-item-' + str(self.first_page) + '"><a class="page-link" href="' \
                + link + str(self.first_page) + queries + '">' + str(self.first_page) + '</a></li>'
            elif show_page_mode == "Q":
                q = ""
                if len(queries) == 0:
                    q = "?page=" + str(self.first_page)
                else: 
                    q = "?page=" + str(self.first_page) + "&" + queries[1:]
                html += '<li class="page-item" id="pag-item-' + str(self.first_page) + '"><a class="page-link" href="' \
                    + link + q +'">' + str(self.first_page) + '</a></li>'
            else:
                html += '<li class="page-item" id="pag-item-' + str(self.first_page) + '"><a class="page-link" href="' \
                    + link + queries + '">' + str(self.first_page) + '</a></li>'

        if self.prev_page - self.first_page > 1:
            if show_page_mode == "U":
                html += '<li class="page-item" id="pag-item-' + str(self.prev_page - 1) + '"><a class="page-link" href="' \
                    + link + str(self.prev_page - 1) + queries + '">&#8592;</a></li>'
            elif show_page_mode == "Q":
                q = ""
                if len(queries) == 0:
                    q = "?page=" + int(self.prev_page - 1)
                else:
                    q = "?page=" + int(self.prev_page - 1) + "&" + queries[1:]
                html += '<li class="page-item" id="pag-item-' + str(self.prev_page - 1) + '"><a class="page-link" href="' \
                    + link + q +'">&#8592;</a></li>'
            else:
                html += '<li class="page-item" id="pag-item-' + str(self.prev_page - 1) + '"><a class="page-link" href="' \
                    + link + queries + '">&#8592;</a></li>'
    
        if self.prev_page != self.page:
            if show_page_mode == "U":
                html  += '<li class="page-item" id="pag-item-' + str(self.prev_page) + '"><a class="page-link" href="' \
                    + link + str(self.prev_page) + queries + '">' + str(self.prev_page) + '</a></li>'
            elif show_page_mode == "Q":
                q = ""
                if len(queries) == 0: 
                    q = "?page=" + str(self.prev_page)
                else:
                    q = "?page=" + str(self.prev_page) + "&" + queries[1:]
                html += '<li class="page-item" id="pag-item-' +str(self.prev_page) + '"><a class="page-link" href="' \
                    + link + q +'">' + str(self.prev_page) + '</a></li>'
            else:
                html += '<li class="page-item" id="pag-item-' + str(self.prev_page) + '"><a class="page-link" href="' \
                    + link.queries + '">' + str(self.prev_page) + '</a></li>'

        html += '<li class="page-item active"><a class="page-link" href="javascript:void(0);">' + str(self.page) \
            + '</a></li>'

        if self.next_page != self.page:
            if show_page_mode == "U":
                html += '<li class="page-item" id="pag-item-' + str(self.next_page) + '"><a class="page-link" href="' \
                    + link + str(self.next_page) + queries + '">' + str(self.next_page) + '</a></li>'
            elif show_page_mode == "Q":
                q = ""
                if len(queries) == 0:
                    q = "?page=" + str(self.next_page)
                else:
                    q = "?page=" + str(self.next_page) + "&" + queries[1:]
                html += '<li class="page-item" id="pag-item-' + str(self.next_page) + '"><a class="page-link" href="' \
                    + link + q +'">' + str(self.next_page) + '</a></li>'
            else:
              html += '<li class="page-item" id="pag-item-' + str(self.next_page) + '"><a class="page-link" href="' \
                + link + queries + '">' + self.next_page + '</a></li>'

        if self.last_page - self.next_page > 1:
            if show_page_mode == "U":
                html += '<li class="page-item" id="pag-item-' + str(self.next_page + 1) + '"><a class="page-link" href="' \
                    + link + str(self.next_page + 1) + queries + '">&#8594;</a></li>'
            elif show_page_mode == "Q":
                q = ""
                if len(queries) == 0:
                    q = "?page=" + str(self.next_page + 1)
                else:
                    q = "?page=" + str(self.next_page + 1) + "&" + queries[1:]
                html += '<li class="page-item" id="pag-item-' + str(self.next_page + 1) + '"><a class="page-link" href="' \
                    + link + q +'">&#8594;</a></li>'
            else:
                html += '<li class="page-item" id="pag-item-' + str(self.next_page + 1) + '"><a class="page-link" href="' \
                    + link + queries + '">&#8594;</a></li>'
    
        if self.last_page != self.next_page:
            if show_page_mode == "U":
                html += '<li class="page-item" id="pag-item-' + "str(self.last_page)" + '"><a class="page-link" href="' \
                    + link + str(self.last_page) + queries + '">' + str(self.last_page) + '</a></li>'
            elif show_page_mode == "Q":
                q = ""
                if len(queries) == 0:
                    q = "?page=" + str(self.last_page)
                else:
                    q = "?page=" + str(self.last_page) + "&" + queries[1:]
                html += '<li class="page-item" id="pag-item-' + str(self.last_page) + '"><a class="page-link" href="' \
                    + link + q + '">' + str(self.last_page) + '</a></li>'
            else:
                html += '<li class="page-item" id="pag-item-' + str(self.last_page) + '"><a class="page-link" href="' \
                    + link + queries + '">' + str(self.last_page) + '</a></li>'

        html += "\n</ul></nav>"
        return html
