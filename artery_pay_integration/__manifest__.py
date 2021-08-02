# -*- coding: utf-8 -*-
{
    'name': 'ArteryPay',
    'version': '1.0',
    'summary': 'ArteryPay Payment Integration',
    'author': 'Socius IGB',
    'company': 'Socius IGB',
    'maintainer': 'Socius IGB',
    'depends': ['point_of_sale', 'sale'],
    'data': [
            'views/artery_pay.xml',
            'views/artery_pay_qr_code.xml',
            'security/ir.model.access.csv',
    ],
    'qweb': [
        # 'static/src/xml/artery_pay_templates.xml'
    ],
    'installable': True,
    'application': False,

}
