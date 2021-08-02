
from odoo import models, fields


class Journal(models.Model):
    _inherit = 'account.journal'

    wechat = fields.Selection([
        ('micropay', 'Scanning customer\'s QR'),
        ('native', 'Showing QR to customer'),
    ], string='WeChat Payment', help='Register for WeChat payment')
