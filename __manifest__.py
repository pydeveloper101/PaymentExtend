# -*- coding: utf-8 -*-
{
    'name': 'Payment Extend',
    'version': '1.3',
    'category': 'Account(dexciss)',
    'sequence': 15,
    'summary': 'Account',
    'description': """Payment information""",
    'author': "Akhodifad",
    'website': "http://dexciss.com/",
    'depends': ['account', 'base','account_pdc'],
    'data': [
        'views/account_payment_view_inherit.xml',
      
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
