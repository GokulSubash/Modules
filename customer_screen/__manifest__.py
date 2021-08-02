
{
    'name': 'Customer Screen',
    'version': '10.0.1.1.0',
    'category': 'Point of Sale',
    'summary': 'POS Screen For Viewing all Orders',
    'author': 'Socius IGB',
    'company': 'Socius',
    'depends': ['point_of_sale', 'pos_retail'],
    'data': [
             'views/pos_template.xml',
             'security/ir.model.access.csv',
            ],
    'qweb': ['static/src/xml/pos_return.xml'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
