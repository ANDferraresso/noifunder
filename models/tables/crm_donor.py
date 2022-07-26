items = {
    "name": "crm_donor",
    "primary": ["rid"],
    "uniques": [["tax_code"]],
    "columnsInUniques": ["tax_code"],
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
        "donor_type": {
            "type": "CHAR",
            "length": "1",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": 1,
            "maxLength": 1,
            "checks": [
                {"func": "isInSet", "pars": ["E", "P"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "name": {
            "type": "VARCHAR",
            "length": "80",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 0,
            "maxLength": 120,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "first_name": {
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
        "last_name": {
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
        "business_name": {
            "type": "VARCHAR",
            "length": "50",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 3,
            "maxLength": 50,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "birth_date": {
            "type": "DATE",
            "length": "",
            "notNull": False,
            "uc_default": "1",
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
        "sex": {
            "type": "CHAR",
            "length": "1",
            "notNull": True,
            "uc_default": "3",
            "default": "",
            "minLength": 1,
            "maxLength": 1,
            "checks": [
                {"func": "isInSet", "pars": ["N", "M", "F"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "tax_code": {
            "type": "VARCHAR",
            "length": "20",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 0,
            "maxLength": 20,
            "checks": [
                {"func": "allowedChars", "pars": ["A-Z0-9"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "vat_number": {
            "type": "VARCHAR",
            "length": "20",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 0,
            "maxLength": 20,
            "checks": [
                {"func": "allowedChars", "pars": ["A-Z0-9"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "country_rid": {
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
        "city": {
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
        "zip_code": {
            "type": "VARCHAR",
            "length": "10",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 5,
            "maxLength": 10,
            "checks": [
                {"func": "isRegex", "pars": ["^[0-9A-Z]*$"]}
            ],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "address_row_1": {
            "type": "VARCHAR",
            "length": "60",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 0,
            "maxLength": 60,
            "checks": [],
            "ui_widget": "",
            "ui_wsUrl": "",
            "ui_wsCallback": ""
        },
        "address_row_2": {
            "type": "VARCHAR",
            "length": "60",
            "notNull": True,
            "uc_default": "2",
            "default": "",
            "minLength": 0,
            "maxLength": 60,
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