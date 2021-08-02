from odoo import models, fields, tools, api, _
from odoo.exceptions import UserError, ValidationError
import datetime


class partnerInherit(models.Model):
    _inherit = 'res.partner'

    otp = fields.Char()
    otp_time = fields.Datetime()
    firstname = fields.Char(string='Name')
    idType = fields.Many2one('new.reach.id', string='Id Type')
    idNumber = fields.Char(string='Id Number')
    lastName = fields.Char(string='Last Name')
    dob = fields.Datetime(string='Date of Birth')
    idExpDate = fields.Datetime(string='Expiration Date')
    issuePlace = fields.Char(string='Country/State Issued')
    image1 = fields.Binary('ID Proof')
    gen = fields.Selection([
         ('male', 'Male'),
         ('female', 'Female'),
     ], string='Sex')
    medicalFirstName = fields.Char(string='First Name')
    medicalLastName = fields.Char(string='Last Name')
    medicalDob = fields.Datetime(string='Date of Birth')
    medicalidNumber = fields.Char(string='Medical ID Card Number')
    medicalIdExpDate = fields.Datetime(string='Expiration Date')
    medicalCounty = fields.Char(string='County of Residence',required=True)
    medicalIssueName = fields.Char(string='Issuing Physicians Name')
    medicalIssueId = fields.Char(string='Issuing Physicians ID')
    medicalImage = fields.Binary('Medical ID/Certificate ')
    medicalCertificateImage = fields.Binary('Physician Letter')

    immatureCannabisPlants = fields.Float(string="Immature Cannabis Plants",readonly=True)
    concentratedCannabis = fields.Float(string="Concentrated cannabis",readonly=True)
    nonConcentratedCannabis = fields.Float(string="Non Concentrated cannabis",readonly=True)
    MedicalCannabis = fields.Float(string="Medical Cannabis",readonly=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Rejected'),
    ], default='pending')
    purchased = fields.One2many('purchase.qty', 'type1', string='purchased')

    def qty_cron(self):
        vals = {'qty':0.0}
        self.env['purchase.qty'].search([]).write(vals)

    @api.model
    def verified_progressbar(self):
        vals = {
            'name': self.name,
            'login': self.email,
            'in_group_10': True,
            'partner_id': self.id
        }

        self.write({
            'state': 'approved',
        })
        self.env['res.users'].create(vals)

    @api.model
    def rejected_progressbar(self):
        self.write({
            'state': 'denied',
        })

class newReachIdType(models.Model):
    _inherit = 'product.category'

    maximumLimitAdult = fields.Float(string="Maximum Adult Limit (Gram)", default=0.0)
    maximumLimitMedical = fields.Float(string="Maximum Medical Limit (Gram)", default=0.0)
    maximumAdultOunce = fields.Float(string="Maximum  Adult Limit(Ounce)", default=0.0)
    maximumMedicalOunce = fields.Float(string="Maximum Medical Limit (Ounce)", default=0.0)

    @api.onchange('maximumAdultOunce')
    def AdultOunceToGram(self):
        ounce = self.maximumAdultOunce
        grams = ounce*28.3495
        self.maximumLimitAdult = round(grams)

    @api.onchange('maximumMedicalOunce')
    def MedOunceToGram(self):
        ounce = self.maximumMedicalOunce
        grams = ounce*28.3495
        self.maximumLimitMedical = round(grams)

    @api.onchange('maximumLimitAdult')
    def AdultGramToOunce(self):
        grams = self.maximumLimitAdult
        ounce = grams/28.3495
        self.maximumAdultOunce = ounce

    @api.onchange('maximumLimitMedical')
    def MedGramToOunce(self):
        grams = self.maximumLimitMedical
        ounce = grams/28.3495
        self.maximumMedicalOunce = ounce

class newReachIdType(models.Model):
    _name = 'new.reach.id'
    _rec_name = "name"

    name = fields.Char(string="Name")
    type = fields.Char(string="Issued State/Country")


class purchaseQty(models.Model):
    _name = 'purchase.qty'

    type1 = fields.Many2one('res.partner', string='Type')
    productCategType = fields.Many2one('product.category', string='Category Type')
    qty = fields.Float(string='Quantity', readonly=True, default=0.0)



