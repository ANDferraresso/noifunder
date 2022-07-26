routes_tree = {
    "ROOT": [
        None,
        {
            "<lang:[a-z]{2}>": [
                ['GET', [], '/root.py', 'Root', 'home'],
                {
                    "acc": [
                        None,
                        {
                            "gift": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/acc_gift.py', 'Acc_Gift', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/acc_gift.py', 'Acc_Gift', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/acc_gift.py', 'Acc_Gift', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "read": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET', [], '/acc_gift.py', 'Acc_Gift', 'read'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/acc_gift.py', 'Acc_Gift', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "pay-method": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/acc_pay_method.py', 'Acc_Pay_Method', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/acc_pay_method.py', 'Acc_Pay_Method', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/acc_pay_method.py', 'Acc_Pay_Method', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "read": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET', [], '/acc_pay_method.py', 'Acc_Pay_Method', 'read'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/acc_pay_method.py', 'Acc_Pay_Method', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "adm": [
                                None,
                                {
                                    "country": [
                                        None,
                                        {
                                            "read": [
                                                None,
                                                {
                                                    "<rid:[1-9]+[0-9]*>": [
                                                        ['GET', [], '/adm_country.py', 'Adm_Country', 'read'],
                                                        None
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "editor": [
                                        None,
                                        {
                                            "read": [
                                                None,
                                                {
                                                    "<rid:[1-9]+[0-9]*>": [
                                                        ['GET', [], '/crm_donor.py', 'Crm_Donor', 'read'],
                                                        None
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "act": [
                        None,
                        {
                            "campaign": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/act_campaign.py', 'Act_Campaign', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/act_campaign.py', 'Act_Campaign', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/act_campaign.py', 'Act_Campaign', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "read": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET', [], '/act_campaign.py', 'Act_Campaign', 'read'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/act_campaign.py', 'Act_Campaign', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "project": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/act_project.py', 'Act_Project', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/act_project.py', 'Act_Project', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/act_project.py', 'Act_Project', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "read": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET', [], '/act_project.py', 'Act_Project', 'read'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/act_project.py', 'Act_Project', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "adm": [
                        None,
                        {
                            "country": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/adm_country.py', 'Adm_Country', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/adm_country.py', 'Adm_Country', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/adm_country.py', 'Adm_Country', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/adm_country.py', 'Adm_Country', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "editor": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/adm_editor.py', 'Adm_Editor', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/adm_editor.py', 'Adm_Editor', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/adm_editor.py', 'Adm_Editor', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/adm_editor.py', 'Adm_Editor', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "crm": [
                        None,
                        {
                            "donor": [
                                None,
                                {
                                    "create": [
                                        ['GET|POST', [], '/crm_donor.py', 'Crm_Donor', 'create'],
                                        None
                                    ],
                                    "delete": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/acc_gift.py', 'Acc_Gift', 'delete'],
                                                None
                                            ]
                                        }
                                    ],
                                    "list": [
                                        None,
                                        {
                                            "<page:[1-9]+[0-9]*>": [
                                                ['GET', [], '/crm_donor.py', 'Crm_Donor', 'list_all'],
                                                None
                                            ]
                                        }
                                    ],
                                    "read": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET', [], '/crm_donor.py', 'Crm_Donor', 'read'],
                                                None
                                            ]
                                        }
                                    ],
                                    "update": [
                                        None,
                                        {
                                            "<rid:[1-9]+[0-9]*>": [
                                                ['GET|POST', [], '/crm_donor.py', 'Crm_Donor', 'update'],
                                                None
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ],
            "": [
                ['GET', [], '/root.py', 'Root', 'home'],
                None
            ]
        }
    ]
}