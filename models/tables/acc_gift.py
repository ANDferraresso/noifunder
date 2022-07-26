items = {
    "name": "acc_gift",
    "primary": ["rid"],
    "uniques": [],
    "columnsInUniques": [],
    "indexes": [],
    "fKeys": {
        "campaign_rid": {"toTable": "act_campaign", "toColumn": "rid", "toRefs": ["code", "title"]}, 
        "pay_method_rid": {"toTable": "acc_pay_method", "toColumn": "rid", "toRefs": ["name"]}, 
        "donor_rid": {"toTable": "crm_donor", "toColumn": "rid", "toRefs": ["name"]}
    },
    "columns": {
        "rid": {
            "type": "SERIAL",
            "length": "",
            "notNull": True,
            "uc_default": "0",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "project_rid": {
            "type": "UINT",
            "length": "",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [
                {"func": "isPositiveInt", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "campaign_rid": {
            "type": "UINT",
            "length": "",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [
                {"func": "isPositiveInt", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "donor_rid": {
            "type": "UINT",
            "length": "",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [
                {"func": "isPositiveInt", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "gift_date": {
            "type": "DATE",
            "length": "0",
            "notNull": True,
            "uc_default": "0",
            "default": "",
            "minLength": 10,
            "maxLength": 10,
            "checks": [
                {"func": "isDate", "pars": ["iso"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "amount": {
            "type": "UDECIMAL",
            "length": "10,2",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": 4,
            "maxLength": 9,
            "checks": [
                {"func": "isEuroMoney", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "pay_method_rid": {
            "type": "UINT",
            "length": "",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [
                {"func": "isPositiveInt", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "memo": {
            "type": "VARCHAR",
            "length": "50",
            "notNull": True,
            "uc_default": "0",
            "default": "",
            "minLength": 0,
            "maxLength": 50,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "creation_dt": {
            "type": "TIMESTAMP",
            "length": "",
            "notNull": True,
            "uc_default": "4",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "creator_rid": {
            "type": "UINT",
            "length": "",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [
                {"func": "isPositiveInt", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        }
    }
}