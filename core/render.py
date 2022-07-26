import math

#
class Render:
    #
    def __init__(self):
        pass

    #
    def _htmlspecialchars(self, text):
        return (
            text.replace("&", "&amp;").
            replace('"', "&quot;").
            replace("<", "&lt;").
            replace(">", "&gt;")
        )

    # 
    def _render_attrs(self, attrs): 
        html = ''
        for k in attrs.keys():
            v = attrs[k]
            if v == None:
                html += " " + k
            else:
                html += " " + k + '="' + str(v) + '"'
        return html 

    #
    def _render_field(self, form_def, gen_t, form_t, v, wrong_fields, k, after_submit):
        html = ""
        hiddens = ""
        js = ""
        
        if not k in form_def['ui']:
            form_def['ui'][k] = { "attrs": {} }
        
        field = form_def['fields'][k]
        field_ui = form_def['ui'][k]

        # Attribuiti (HTML) comuni
        if k == "_csrf":
            field_ui['attrs']['name'] = form_def['prefix'] + k
            field_ui['attrs']['id'] = form_def['prefix'] + k + "_id"
        else:
            field_ui['attrs']['name'] = form_def['prefix'] + k
            field_ui['attrs']['id'] = form_def['prefix'] + k + "_id"

        html = ""
        js = ""

        # Escape 
        v = self._htmlspecialchars(v)
        # Widget
        if field_ui['widget'] == "reCAPTCHA-v2-Checkbox":
            # Google CATPCHA reCAPTCHA v2 Checkbox
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label>'
            html += "\n" + '<div class="g-recaptcha" data-sitekey="' + field_ui['default'] + '"></div>'
            if after_submit:
                if k in wrong_fields:
                    html += "\n" + '<div class="invalid-feedback d-block">' + form_t['msg'][k] + '</div>'
                else:
                    html += "\n" + '<div class="valid-feedback d-block"></div>'
                
            if k in form_t['info'] and form_t['info'][k] != '':
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'
    
        # INPUT-FILE
        elif field_ui['widget'] == "input-file":
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else:
                field_ui['attrs']['class'] += " form-control form-control-sm"
                if after_submit:
                    if k in wrong_fields: 
                        field_ui['attrs']['class'] += " is-invalid"
                    else:
                        field_ui['attrs']['class'] += " is-valid"
                field_ui['attrs']['aria-describedby'] = form_def['prefix'] + k + '_helpBlock'
                field_ui['attrs']['type'] = "file"
                field_ui['attrs']['value'] = v
                if field['maxLength'] != None: 
                    field_ui['attrs']['maxlength'] = field['maxLength']
                html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><input' + self._render_attrs(field_ui['attrs']) + ' />'
                if after_submit:
                    if k in wrong_fields: 
                        html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                    else:
                        html += "\n" + '<div class="valid-feedback"></div>'
                if k in form_t['info'] and form_t['info'][k] != '': 
                    html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'

        # INPUT-HIDDEN
        elif field_ui['widget'] == "input-hidden":
            field_ui['attrs']['type'] = "hidden"
            field_ui['attrs']['value'] = v
            if field['maxLength'] != None: 
                field_ui['attrs']['maxlength'] = field['maxLength']
            hiddens += "\n" + '<input ' + self._render_attrs(field_ui['attrs']) + ' />'
        
        # INPUT-PASSWORD
        elif field_ui['widget'] == "input-password":
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else:
                field_ui['attrs']['class'] += " form-control form-control-sm"
                if after_submit:
                    if k in wrong_fields: 
                        field_ui['attrs']['class'] += " is-invalid"
                    else:
                        field_ui['attrs']['class'] += " is-valid"
                field_ui['attrs']['aria-describedby'] = form_def['prefix'] + k + '_helpBlock'
                field_ui['attrs']['type'] = "password"
                field_ui['attrs']['value'] = v
                if field['maxLength'] != None: 
                    field_ui['attrs']['maxlength'] = field['maxLength']
                html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><input' + self._render_attrs(field_ui['attrs']) + ' />'
                if after_submit:
                    if k in wrong_fields: 
                        html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                    else:
                        html += "\n" + '<div class="valid-feedback"></div>'
                if k in form_t['info'] and form_t['info'][k] != '': 
                    html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'
         
        # INPUT-CHECKBOX 
        elif field_ui['widget'] == "input-checkbox":
            check_box_label = ""
            for i in field_ui['options']:
                if len(i) == 0:
                    pass
                else:
                    opt_k = list( i.keys() )[0]
                    opt_v = i[opt_k]
                    if str(opt_k) == "1":
                        check_box_label = opt_v
                        break

            html += "\n" + '<label class="form-label">' + field['title'] + '</label>'
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = ""
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else:
                    field_ui['attrs']['class'] += " is-valid"
            field_ui['attrs']['type'] = "checkbox"
            field_ui['attrs']['value'] = "1"
            if v == "1":
                field_ui['attrs']['checked'] = "checked"
            html += '<div class="form-check"><label for="' + field_ui['attrs']['id'] + '">' \
                + check_box_label \
                + '</label>&nbsp;<input' + self._render_attrs(field_ui['attrs']) + ' />'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else:
                    html += "\n" + '<div class="valid-feedback"></div>'
            html += "\n" + "</div>"
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'

        # INPUT-RADIO
        elif field_ui['widget'] == "input-radio":
            html += "\n" + '<label class="form-label">' + field['title'] + '</label>'
            radios = ""
            radio_c = 0
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = ""
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else:
                    field_ui['attrs']['class'] += " is-valid"
            for i in field_ui['options']:
                if len(i) == 0:
                    pass
                else:
                    opt_k = list( i.keys() )[0]
                    opt_v = i[opt_k]
                    if v == str(opt_k):
                        radios += '<div class="form-check"><input class="form-check-input" type="radio" name="' \
                        + form_def['prefix'] + k + '" id="' + form_def['prefix'] + k + '_id_' \
                        + str(radio_c) + '" value="' + str(opt_k) + '" checked="checked" /><label class="form-check-label" for="' \
                        + form_def['prefix'] + k + '_id_' + str(radio_c) + '">' + opt_v +'</label></div>'
                    else:
                        radios += '<div class="form-check"><input class="form-check-input" type="radio" name="' \
                        + form_def['prefix'] + k + '" id="' + form_def['prefix'] + k + '_id_'  \
                        + str(radio_c) + '" value="' + str(opt_k) + '" /><label class="form-check-label" for="' \
                        + form_def['prefix'] + k + '_id_' + str(radio_c) + '">' + opt_v + '</label></div>'
                    radio_c += 1
            html += radios
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback d-block">' + form_t['msg'][k] + '</div>'
                else:
                    html += "\n" + '<div class="valid-feedback d-block"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'

        # SELECT
        elif field_ui['widget'] == "select":
            options = ""
            for i in field_ui['options']:
                if len(i) == 0:
                    pass
                else:
                    opt_k = list( i.keys() )[0]
                    opt_v = i[opt_k]
                    if v == str(opt_k):
                        options += '<option value="' + str(opt_k) + '" selected="selected">' + opt_v + '</option>'
                    else:
                        options += '<option value="' + str(opt_k) + '">' + opt_v + '</option>'
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-select form-select-sm"
            else: 
                field_ui['attrs']['class'] += " form-select form-select-sm"
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else: 
                    field_ui['attrs']['class'] += " is-valid"
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><select' + self._render_attrs(field_ui['attrs']) + '>' + options + '</select>'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else: 
                    html += "\n" + '<div class="valid-feedback"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'

        # SELECT-SEARCH
        elif field_ui['widget'] == "select-search":
            options = ""
            for i in field_ui['options']:
                if len(i) == 0:
                    pass
                else:
                    opt_k = list( i.keys() )[0]
                    opt_v = i[opt_k]
                    if str(v) == opt_k:
                        options += '<option value="' + str(opt_k) + '" selected="selected">' + opt_v + '</option>'
                    else:
                        options += '<option value="' + str(opt_k) + '">' + opt_v + '</option>'
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else: 
                field_ui['attrs']['class'] += " form-control form-control-sm"
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else: 
                    field_ui['attrs']['class'] += " is-valid"
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><select' + self._render_attrs(field_ui['attrs']) + '>' + options + '</select>'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else: 
                    html += "\n" + '<div class="valid-feedback"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'
            html += "\n" + '<div class="input-group input-group-sm mt-1"><input id="' + form_def['prefix'] + k + '_search-txt" class="form-control form-control-sm" maxlength="10" /><div class="input-group-append"><button class="btn btn-outline-secondary" type="button" id="' + form_def['prefix'] + k + '_search-btn"><span class="oi oi-magnifying-glass"></span></button></div></div>'
            js += '' # DA FARE

        # TEXTAREA
        elif field_ui['widget'] == "textarea":
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else:
                field_ui['attrs']['class'] += " form-control form-control-sm"
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else: 
                    field_ui['attrs']['class'] += " is-valid"
            # field_ui['attrs']['aria-describedby'] = form_def['prefix'] + k + '_helpBlock'
            if field['maxLength'] != None: 
                field_ui['attrs']['maxlength'] = field['maxLength']
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><textarea' + self._render_attrs(field_ui['attrs']) + ' onkeyup="keyup_' + form_def['prefix'] + k + '();">' + v + '</textarea>'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else: 
                    html += "\n" + '<div class="valid-feedback"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'
            html += '<div><span class="badge bg-secondary" id="' + form_def['prefix'] + k + '_chars_counter_id' + '">' + str(field_ui['attrs']['maxlength']) + '</span></div>'
            js += "\n" + 'document.getElementById("' + form_def['prefix'] + k + '_chars_counter_id").innerHTML = parseInt(document.getElementById("' + form_def['prefix'] + k + '_id").getAttribute("maxlength")) - parseInt(document.getElementById("' + form_def['prefix'] + k + '_id").value.length);'
            js += "\n" + 'function keyup_' + form_def['prefix'] + k + '() {'
            js += "\n" + '  document.getElementById("' + form_def['prefix'] + k + '_id").value = document.getElementById("' + form_def['prefix'] + k + '_id").value.substring(0, parseInt(document.getElementById("' + form_def['prefix'] + k + '_id").getAttribute("maxlength")));'
            js += "\n" + '  document.getElementById("' + form_def['prefix'] + k + '_chars_counter_id").innerHTML = parseInt(document.getElementById("' + form_def['prefix'] + k + '_id").getAttribute("maxlength")) - parseInt(document.getElementById("' + form_def['prefix'] + k + '_id").value.length);'
            js += "\n" + '}'
            js += "\n"
            
        # INPUT-EMAIL
        elif field_ui['widget'] == "input-email":
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else:
                field_ui['attrs']['class'] += " form-control form-control-sm"
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else: 
                    field_ui['attrs']['class'] += " is-valid"    
            field_ui['attrs']['aria-describedby'] = form_def['prefix'] + k + '_helpBlock'
            field_ui['attrs']['type'] = "email"
            field_ui['attrs']['value'] = v
            if field['maxLength'] != None: 
                field_ui['attrs']['maxlength'] = field['maxLength']
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><input' + self._render_attrs(field_ui['attrs']) + ' />'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else: 
                    html += "\n" + '<div class="valid-feedback"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'

        # INPUT-DATE
        elif field_ui['widget'] == "input-date":
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else: 
                field_ui['attrs']['class'] += " form-control form-control-sm"
            if after_submit:
                if k in wrong_fields: 
                    field_ui['attrs']['class'] += " is-invalid"
                else: 
                    field_ui['attrs']['class'] += " is-valid"
            field_ui['attrs']['aria-describedby'] = form_def['prefix'] + k + '_helpBlock'
            field_ui['attrs']['type'] = "date"
            field_ui['attrs']['value'] = v
            field_ui['attrs']['maxlength'] = "10"
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><input' + self._render_attrs(field_ui['attrs']) + ' />'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else: 
                    html += "\n" + '<div class="valid-feedback"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>';
            js += '' # DA FARE

        # // INPUT-TEXT
        else:
            if not "class" in field_ui['attrs']:
                field_ui['attrs']['class'] = "form-control form-control-sm"
            else:
                field_ui['attrs']['class'] += " form-control form-control-sm"
            if after_submit:
                if k in wrong_fields:
                    field_ui['attrs']['class'] += " is-invalid"
                else:
                    field_ui['attrs']['class'] += " is-valid"
            field_ui['attrs']['aria-describedby'] = form_def['prefix'] + k + '_helpBlock'
            field_ui['attrs']['type'] = "text"
            field_ui['attrs']['value'] = v
            if field['maxLength'] != None:
                field_ui['attrs']['maxlength'] = field['maxLength']
            html += "\n" + '<label class="form-label" for="' + field_ui['attrs']['id'] + '">' + field['title'] + '</label><input' + self._render_attrs(field_ui['attrs']) + ' />'
            if after_submit:
                if k in wrong_fields: 
                    html += "\n" + '<div class="invalid-feedback">' + form_t['msg'][k] + '</div>'
                else: 
                    html += "\n" + '<div class="valid-feedback"></div>'
            if k in form_t['info'] and form_t['info'][k] != '': 
                html += "\n" + '<small id="' + form_def['prefix'] + k + '_helpBlock" class="form-text text-muted">' + form_t['info'][k] + '</small>'
       
        return html, hiddens, js

    #
    def render_form(self, form_def, gen_t, form_t, display, form_attrs, f_values, wrong_fields, use_defaults,
        before_form_closing, after_submit, bnt_class, bnt_text):

        # Main loop
        html = ""
        html += "\n<form " + self._render_attrs(form_attrs) + '>'

        hiddens = ""
        js = ""

        f_values_keys = list(f_values.keys())
        if len(display) == 0:
            cc = 0
            for k in form_def['fields']:
                field_ui = form_def['ui'][k]
                value = ""
                if k in f_values_keys:
                    if f_values[k] == None:
                        value = ""
                    else:
                        value = str(f_values[k])
                elif use_defaults and "default" in field_ui and field_ui['default'] is not None:
                    value = str(field_ui['default'])
                elif "value" in field_ui['attrs']:
                    value = str(field_ui['attrs']['value'])

                f_html, f_hiddens, f_js = self._render_field(form_def, gen_t, form_t, value, wrong_fields, k, after_submit)
                if f_html != '':
                    html += "\n" + '<div id="form-' + form_def['prefix'] + 'row' + "_" + str(cc) + '" class="row g-2 mb-2">'
                    html += "\n" + '<div class="col" id="' + form_def['prefix'] + k + '_form-group">'
                    html += f_html
                    html += "\n" + '</div><!-- /col -->'
                    html += "\n" + '</div><!-- /row -->'
                    cc += 1
                hiddens += f_hiddens
                js += f_js
        else:
            cc = 0
            for row in display:
                tmp_html = ""
                i = 0
                while i < len(row):
                    k = row[i]
                    field_ui = form_def['ui'][k]
                    value = ""
                    if k in f_values_keys:
                        if f_values[k] == None:
                            value = ""
                        else:
                            value = str(f_values[k])
                    elif use_defaults and "default" in field_ui and field_ui['default'] is not None:
                        value = str(field_ui['default'])
                    elif "value" in field_ui['attrs']:
                        value = str(field_ui['attrs']['value'])

                    f_html, f_hiddens, f_js = self._render_field(form_def, gen_t, form_t, value, wrong_fields, k, after_submit)
                    if f_html != '':
                        tmp_html += "\n" + '<div class="col-md-' + str(row[i + 1]) + '" id="' + form_def['prefix'] + row[i] + '_form-group">'
                        tmp_html += f_html
                        tmp_html += "\n" + '</div><!-- /col -->'
                    hiddens += f_hiddens
                    js += f_js
                    i += 2
                if tmp_html != '':
                    html += "\n" + '<div class="row g-2 mb-2" id="form-' + form_def['prefix'] + 'row' + "_" + str(cc) + '">'
                    html += tmp_html
                    html += "\n" + '</div><!-- /row -->'
                    cc += 1

        html += "\n" + hiddens
        if len(bnt_class) == 0:
            bnt_class = "btn btn-primary"
        html += "\n<div class=\"row mt-2\">\n<div class=\"col\">\n" + '<button type="submit" class="' + bnt_class + '" name="submit-button" id="submit-button_id">' + bnt_text + '</button>' + "\n</div><!-- /col -->\n</div><!-- /row -->"
        if before_form_closing != '': 
            html += "\n" + before_form_closing
        html += "\n</form>"
  
        return html, js

    #
    def render_record(self, table_columns_keys, table_fKeys, T, data, ext_refs, f_key_links, quick_list, escape_html, view_mode):
        table_cls = table_columns_keys
        columns = []
        if len(quick_list) > 0:
            columns = quick_list
        else:
            for v in table_cls:
                columns.append(v)

        html = ""
        if view_mode == 1:
            html = '<table class="table table-sm table-striped table-hover table-responsive w-auto text-nowrap">' + "\n<tbody>"
            c_l = 0
            c_r = math.ceil(len(columns) / 2)
            while c_l < math.ceil(len(columns) / 2):
                v = columns[c_l]
                html += "\n<tr>"
                html += "\n" + '<th scope="row">' + T['title'][v] + '</th>'
                if ext_refs and v in table_fKeys:
                    if v in escape_html:
                        html += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + self._htmlspecialchars(str(data[0][v +'_FK'])) + '</a></td>'
                    else:
                        html += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + str(data[0][v + '_FK']) + '</a></td>' 
                else:
                    if v in escape_html: 
                        html += "\n" + '<td>' + self._htmlspecialchars(str(data[0][v])) + '</td>'
                    else:
                        html += "\n" + '<td>' + str(data[0][v]) + '</td>'
                if c_r < len(columns):
                    v = columns[c_r]
                    html += "\n" + '<th scope="row">' + T['title'][v] + '</th>'
                    if ext_refs and v in table_fKeys:
                        if v in escape_html:
                            html += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + self._htmlspecialchars(str(data[0][v + '_FK'])) + '</a></td>'
                        else:
                            html += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + str(data[0][v + '_FK']) + '</a></td>'
                    else:
                        if v in escape_html:
                            html += "\n" + '<td>' + self._htmlspecialchars(str(data[0][v])) + '</td>'
                        else:
                            html += "\n" + '<td>' + str(data[0][v]) + '</td>'
                    html += "\n</tr>"
                else:
                    html += "\n" + '<th scope="row"></th>'
                    html += "\n" + '<td>&nbsp;</td>'
                    html += "\n</tr>"

                c_l += 1
                c_r += 1
            html += "\n</tbody>\n</table>"
        elif view_mode == 2:
            html_L = '<table class="table table-sm table-striped table-hover">' + "\n<tbody>"
            html_R = '<table class="table table-sm table-striped table-hover">' + "\n<tbody>"
            c_l = 0
            c_r = math.ceil(len(columns) / 2)
            while c_l < math.ceil(len(columns) / 2):
                v = columns[c_l]
                html_L += "\n<tr>"
                html_L += "\n" + '<th scope="row">' + T['title'][v] + '</th>'
                if ext_refs and v in table_fKeys:
                    if v in escape_html:
                        if v in f_key_links:
                            html_L += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + self._htmlspecialchars(str(data[0][v + '_FK'])) + '</a></td>'
                        else:
                            html_L += "\n" + '<td>' + self._htmlspecialchars(str(data[0][v + '_FK'])) + '</td>'
                    else:
                        if v in f_key_links:
                            html_L += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + str(data[0][v + '_FK']) + '</a></td>'
                        else:

                            html_L += "\n" + '<td>' + str(data[0][v + '_FK']) + '</td>'
                else:
                    if v in escape_html:
                        html_L += "\n" + '<td>' + self._htmlspecialchars(str(data[0][v])) + '</td>'
                    else:
                        pass
                        html_L += "\n" + '<td>' + str(data[0][v]) + '</td>'

                html_L += "\n</tr>"
                if c_r < len(columns):
                    v = columns[c_r]
                    html_R += "\n<tr>"
                    html_R += "\n" + '<th scope="row">' + T['title'][v] + '</th>'
                    if ext_refs and v in table_fKeys:
                        if v in escape_html:
                            if v in f_key_links:
                                html_R += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + self._htmlspecialchars(str(data[0][v + '_FK'])) + '</a></td>'
                            else:
                                html_R += "\n" + '<td>' + self._htmlspecialchars(str(data[0][v + '_FK'])) + '</td>' 
                        else:
                            if v in f_key_links:
                                html_R += "\n" + '<td><a href="' + f_key_links[v] + '/' + str(data[0][v]) + '">' + str(data[0][v + '_FK']) + '</a></td>'
                            else:
                                html_R += "\n" + '<td>' + str(data[0][v + '_FK']) + '</td>'
                    else:
                        if v in escape_html:
                            html_R += "\n" + '<td>' + self._htmlspecialchars(str(data[0][v])) + '</td>'
                        else:
                            html_R += "\n" + '<td>' + str(data[0][v]) + '</td>'                            
                    html_R += "\n</tr>"
                else:
                    html_R += "\n<tr>"
                    html_R += "\n" + '<th scope="row"></th>'
                    html_R += "\n" + '<td>&nbsp;</td>'
                    html_R += "\n</tr>"
                c_l += 1
                c_r += 1
            html_R += "\n</tbody>\n</table>"
            html_L += "\n</tbody>\n</table>"
            html += "\n" + '<div class="row">'
            html += "\n" + '<div class="col">'
            html += "\n" + html_L
            html += "\n" + '</div>'
            html += "\n" + '<div class="col">'
            html += "\n" + html_R
            html += "\n" + '</div>'
            html += "\n" + '</div><!-- /row -->'
        return html   