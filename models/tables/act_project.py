items = {
    "name": "act_project",
    "primary": ["rid"],
    "uniques": [["code"], ["title"]],
    "columnsInUniques": ["code", "title"],
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
        "code": {
            "type": "CHAR",
            "length": "6",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 6,
            "maxLength": 6,
            "checks": [
                {"func": "allowedChars", "pars": ["A-Za-z0-9"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "title": {
            "type": "VARCHAR",
            "length": "30",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 5,
            "maxLength": 30,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "status": {
            "type": "CHAR",
            "length": "1",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": 1,
            "maxLength": 1,
            "checks": [
                {"func": "isInSet", "pars": ["O", "C", "S", "D"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "start_date": {
            "type": "DATE",
            "length": "",
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
        "deadline": {
            "type": "DATE",
            "length": "",
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
        "memo": {
            "type": "TEXT",
            "length": "1000",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 0,
            "maxLength": 1000,
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