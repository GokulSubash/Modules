from odoo import models, fields


class User_type(models.Model):

    _inherit = 'res.partner'

    customer_type = fields.Selection([('adult_customer', 'Adult Recreation Customer'),
                                     ('medical_customer', 'Medical Customer')], string='Type of Customer')
