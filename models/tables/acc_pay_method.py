items = {
    "name": "acc_pay_method",
    "primary": ["rid"],
    "uniques": [["name"]],
    "columnsInUniques": ["name"],
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
            "minLength": 3,
            "maxLength": 50,
            "checks": [
                {"func": "allowedChars", "pars": ["A-Za-z0-9\\.\\- "]}
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