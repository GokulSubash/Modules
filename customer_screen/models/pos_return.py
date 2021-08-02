# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo import models, fields, tools, api, _

class PosPaymentStatus(models.Model):

    _name = 'pos.payment_status'

    order_number = fields.Char(string='Order Id')
    customer_id = fields.Char(string='Customer Id')
    customer_name = fields.Char(string='Customer Name')
    sales_amount = fields.Char(string='Amount')
    status = fields.Char(string='Status')
    delivery_status = fields.Char(string='Delivery Status')

    @api.model
    def payment_status(self, bill, order_id, client, client_name):

        vals = {
            'order_number': order_id,
            'customer_id': client,
            'customer_name': client_name,
            'sales_amount': bill,
            'product_status': 'Pending',
        }
        payment = self.env['pos.payment_status'].search([('customer_id', '=', client)])

        if not payment:
            self.env['pos.payment_status'].create(vals)

        if payment:
            payment.write({
                'order_number': order_id,
                'sales_amount': bill,
                'status': 'Pending',
                'delivery_status': 'Pending',
               })

        return True


class PosOrderData(models.Model):

    _inherit = 'pos.order'

    @api.model
    def get_pos_order_data(self):
        pos_order = self.env['pos.order'].search([])
        pos_data = []
        if pos_order:
            for i in pos_order:
                values = {}
                values['id'] = i.id
                values['name'] = i.name
                values['partner_id'] = [i.partner_id.id, i.partner_id.name]
                values['state'] = i.state
                values['amount_total'] = i.amount_total
                values['product_status'] = i.product_status
                values['payment_status'] = i.payment_status
                values['delivery_status'] = i.delivery_status
                pos_data.append(values)

            return pos_data
        else:
            return 0


class SaleOrderData(models.Model):

    _inherit = 'sale.order'

    @api.model
    def get_sale_order_data(self):
        sale_order = self.env['sale.order'].search([])
        sale_data = []
        if sale_order:
            for i in sale_order:
                values = {}
                values['id'] = i.id
                values['name'] = i.name
                values['date_order'] = i.date_order
                values['amount_total'] = i.amount_total
                values['partner_id'] = [i.partner_id.id, i.partner_id.name]
                values['product_status'] = i.product_status
                values['payment_status'] = i.payment_status
                values['delivery_status'] = i.delivery_status
                values['team_id'] = [i.team_id.id, i.team_id.name]
                sale_data.append(values)
            return sale_data
        else:
            return 0
