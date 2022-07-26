import core.form_validator

#
class Form:
    #
    def __init__(self, ctx):
        self.ctx = ctx
        self.table_def = None
        self.form_def = { 
            "name": "",
            "prefix": "",
            "required": [],
            "dontValidate": [],
            "fields": {},
            "ui": {}
        }

    #
    def add_field(self, key, title): 
        self.form_def['fields'][key] = {
            "name": key,
            "title": title,
            "minLength": None,
            "maxLength": None,
            "checks": [],
        }

        self.form_def['ui'][key] = {
            "attrs": {},
            "default": "",
            "widget": "input-text",
            "wsUrl": "",
            "wsCallback": "",
            "options": []
        }

        return

    #
    def add_csrf_field(self): 
        self.form_def['fields']['_csrf'] = {
            "name": '_csrf', 
            "title": '', 
            "minLength": None, 
            "maxLength": None, 
            "checks": []
        }
        self.form_def['ui']['_csrf'] = {
            "attrs": {
                "value": ""
            },
            "default": None, 
            "widget": 'input-hidden', 
            "wsUrl": "", 
            "wsCallback": "",
            "options": []

        }

        return

    #
    def import_table(self, table_def, table_T, ext_refs, quick_list, not_required, prefix):  
        table_cls = list(table_def['columns'].keys())
        columns = []
        if len(quick_list) > 0:
            columns = quick_list
        else:
            for v in table_cls:
                columns.append(v)
        self.form_def['name'] = table_def['name']
        self.form_def['prefix'] = prefix
        self.form_def['required'] = []
        self.form_def['dontValidate'] = []
        self.form_def['fields'] = {}
        self.form_def['ui'] = {}

        for v in columns:
            self.import_column(table_def, table_T, v, ext_refs, not_required)

        # Add _csrf
        self.add_csrf_field()
        return

    #
    def import_column(self, table_def, table_T, c_key, ext_refs, not_required):
        column = table_def['columns'][c_key]
        self.form_def['fields'][c_key] = {
            "name": c_key,
            "title": table_T['title'][c_key],
            "minLength": column['minLength'],
            "maxLength": column['maxLength'],
            "checks": column['checks']
        }

        self.form_def['ui'][c_key] = {
            "attrs": {}, 
            "default": "", 
            "widget": "", 
            "wsUrl": "", 
            "wsCallback": "",
            "options": []
        }

        # default
        if column['default'] != None:
            self.form_def['ui'][c_key]['default'] = column['default']

        if c_key in table_T['opts']:
            self.form_def['ui'][c_key]['options'] = table_T['opts'][c_key]
                
        if column['ui_widget'] == "input-checkbox": 
            if c_key in not_required:
                pass
            else:
                self.form_def['required'].append(c_key)
                self.form_def['ui'][c_key]['attrs']['required'] = "required"
        else:
            if c_key in not_required:
                pass
            else:
                self.form_def['required'].append(c_key)
                self.form_def['ui'][c_key]['attrs']['required'] = "required"

        if column['ui_widget'] != "":
            self.form_def['ui'][c_key]['widget'] = column['ui_widget']
        if column['ui_wsUrl'] != "":
            self.form_def['ui'][c_key]['wsUrl'] = column['ui_wsUrl']
        if column['ui_wsCallback'] != "":
            self.form_def['ui'][c_key]['wsCallback'] = column['ui_wsCallback']; 

        return

    #
    def validate_one(self, k, value):
        validator = core.form_validator.Form_Validator()
        field = self.form_def['fields'][k]
        if k in self.form_def['dontValidate']:
            return True
        # minLength
        if field['minLength'] != None:
            if not validator.isMinLength(value, [ int(field['minLength']) ]):
                return False
        # maxLength
        if field["maxLength"] != None:
            if not validator.isMaxLength(value, [ int(field['maxLength']) ]):
                return False
        # Checks
        for check in field['checks']:
            if check != "":
                func = check['func']
                pars = check['pars']
                if not getattr(validator, check['func'])( value, check['pars'] ):
                    return False
            
        return True

    #
    def validate_all(self):
        f_values = {}
        wrong_fields = []

        for k in self.form_def['fields']:
            if k == '_csrf':
                pass
            else:
                if not self.form_def['prefix'] + k in self.ctx['post_vars']:
                    # Param isn't present
                    if k in self.form_def['required']:
                        f_values[k] = ""
                        # Se la lunghezza minima consentita è 0 (o null) e l'input ha lunghezza 0, non lo validare
                        if self.form_def['fields'][k]['minLength'] in (None, 0):
                            pass
                        else:
                            if not self.validate_one(k, f_values[k]):
                                wrong_fields.append(k)
                else:
                    f_values[k] = self.ctx['post_vars'][ self.form_def['prefix'] + k ].strip()
                    # Se la lunghezza minima consentita è 0 (o null) e l'input ha lunghezza 0, non lo validare
                    if (self.form_def['fields'][k]['minLength'] in (None, 0)) and f_values[k] == "":
                        pass
                    else:
                        if not self.validate_one(k, f_values[k]):
                            wrong_fields.append(k)

        return f_values, wrong_fields

    # 
    def _render_attrs(attrs): 
        html = ''
        for k in attrs:
            v = attrs[k]
            if v == None:
                html += " " + k
            else:
                html += " " + k + '="' + str(v) + '"'
        return html 