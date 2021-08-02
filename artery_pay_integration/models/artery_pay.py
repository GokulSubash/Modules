from odoo import models, fields, api, _
import logging
import qrcode
import base64
from io import BytesIO

_logger = logging.getLogger(__name__)


class ArteryPay(models.Model):
    _name = 'artery.pay'

    merchant_handle = fields.Char("Merchant Handle")
    WebHook_secret = fields.Char('WebHook Secret Key')


class ArteryPayHistory(models.Model):
    _name = 'artery.pay.history'

    purchase_id = fields.Char("Purchase Id")
    order_id = fields.Char("Order Id")
    order_amount = fields.Char("Total Amount")
    order_type = fields.Selection(selection=[("pos", "Point of Sale"),
                                             ("mobile", "Mobile"), ("website", "Website")], string="Order Type")
    payment_status = fields.Selection(selection=[("completed", "Completed"), ("failed", "Failed"),
                                                 ("waiting", "Waiting")], string="Payment Status")


class ArteryPayQRCodePOS(models.Model):
    _inherit = 'pos.order'

    artery_pay_QR = fields.Binary("ArteryPay QrCode")

    @api.model
    def create(self, vals):
        pos = super(ArteryPayQRCodePOS, self).create(vals)
        receipt = []
        merchant_handle = self.env['artery.pay'].search([], limit=1).merchant_handle
        external_purchase_id = pos.name
        total_cents = pos.amount_total * 100
        if pos.lines:
            for i in pos.lines:
                line = {
                    'item': i.product_id.name,
                    'count': i.qty,
                    'price': i.price_subtotal
                }
                receipt.append(line)
        data = {
            "name": "artery",
            "type": "purchase",
            "version": 1,
            "properties": {
                "merchant_handle": merchant_handle,
                "external_purchase_id": external_purchase_id,
                "total_cents": total_cents,
                "receipt": receipt
            }
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        artery_pay_QR = base64.b64encode(temp.getvalue())
        pos.artery_pay_QR = artery_pay_QR
        return pos


class ArteryPayQRCodeSO(models.Model):
    _inherit = 'sale.order'

    artery_pay_QR = fields.Binary("ArteryPay QrCode")

    @api.model
    def create(self, vals):
        sale = super(ArteryPayQRCodeSO, self).create(vals)
        receipt = []

        if sale.order_line:
            for i in sale.order_line:
                line = {
                    'item': i.product_id.name,
                    'count': i.product_uom_qty,
                    'price': i.price_subtotal
                }
                receipt.append(line)
        external_purchase_id = sale.name
        merchant_handle = self.env['artery.pay'].search([], limit=1).merchant_handle
        total_cents = sale.amount_total * 100
        data = {
            "name": "artery",
            "type": "purchase",
            "version": 1,
            "properties": {
                "merchant_handle": merchant_handle,
                "external_purchase_id": external_purchase_id,
                "total_cents": total_cents,
                "receipt": receipt
            }
        }
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        artery_pay_QR = base64.b64encode(temp.getvalue())
        vals['artery_pay_QR'] = artery_pay_QR
        sale.artery_pay_QR = artery_pay_QR
        return sale
