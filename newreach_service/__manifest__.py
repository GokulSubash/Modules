{
    'name': "New Reach Service",
    'version': '1.0',
    'author': "Socius IGB",
    'category': 'Generic Modules',
    'website': 'sociusigb.in',
    'summery': '',
    'demo': [],
    'images': [
        'static/description/icon.jpg',
    ],
    'depends': ['base', 'hr', 'sale', 'purchase'],
    'data': [
        'views/partnerInherit.xml',
        'views/idType.xml',
        'views/user_type.xml',
        'views/Medical_viewForm.xml',
        'views/cronview.xml',
        'views/purchase_qty.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
