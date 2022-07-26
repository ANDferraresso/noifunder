items = {
    "name": "adm_country",
    "primary": ["rid"],
    "uniques": [["name"], ["code"]],
    "columnsInUniques": ["name", "code"],
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
            "uc_default": "0",
            "default": "",
            "minLength": 2,
            "maxLength": 50,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "code": {
            "type": "CHAR",
            "length": "2",
            "notNull": True,
            "uc_default": "0",
            "default": "",
            "minLength": 2,
            "maxLength": 2,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "eu": {
            "type": "UTINYINT",
            "length": "1",
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
        "currency": {
            "type": "VARCHAR",
            "length": "3",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 3,
            "maxLength": 3,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "active": {
            "type": "UTINYINT",
            "length": "1",
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