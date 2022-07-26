items = {
    "name": "adm_editor",
    "primary": ["rid"],
    "uniques": [["email"]],
    "columnsInUniques": ["email"],
    "indexes": [],
    "fKeys": {},
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
        "name": {
            "type": "VARCHAR",
            "length": "50",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 2,
            "maxLength": 50,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "email": {
            "type": "VARCHAR",
            "length": "60",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 5,
            "maxLength": 60,
            "checks": [
                {"func": "isEmail", "pars": []}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "active": {
            "type": "UTINYINT",
            "length": "",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": 1,
            "maxLength": 1,
            "checks": [
                {"func": "allowedChars", "pars": ["0-1"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "last_login": {
            "type": "DATETIME",
            "length": "",
            "notNull": False,
            "uc_default": "1",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "last_logout": {
            "type": "DATETIME",
            "length": "",
            "notNull": False,
            "uc_default": "1",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "session_token": {
            "type": "VARCHAR",
            "length": "255",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "session_token_dl": {
            "type": "UBIGINT",
            "length": "",
            "notNull": False,
            "uc_default": "1",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "email_token": {
            "type": "VARCHAR",
            "length": "255",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": None,
            "maxLength": None,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "email_token_dl": {
            "type": "UBIGINT",
            "length": "",
            "notNull": False,
            "uc_default": "1",
            "default": "",
            "minLength": None,
            "maxLength": None,
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