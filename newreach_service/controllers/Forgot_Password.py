from odoo.http import request
from odoo import http
import smtplib
import datetime
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import random
import logging
import hashlib

_logger = logging.getLogger(__name__)


class reset_password_employee(http.Controller):

    @http.route('/employee/reset_password', methods=['POST'], auth='public', csrf=False)
    def get_email_id(self, **kwargs):
        email_id = kwargs.get('email')
        users = request.env['res.users'].sudo().search([('login', '=', str(email_id))])
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', users.id)])
        if employee:

            otp = random.randint(1000, 9999)
            otp_time = datetime.datetime.now()
            user_name = users.name

            mail = request.env['ir.mail_server'].sudo().search([], limit=1)
            port = mail.smtp_port  # For SSL
            user = mail.smtp_user
            user_password = mail.smtp_pass
            server = mail.smtp_host
            msg = MIMEMultipart()
            msg['From'] = user
            msg['To'] = email_id
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = str(otp) + ' is your PureCannabis employee app password recovery code '
            body = 'Hi ' + user_name + ',\n\n We received a request to reset your Purecannabis employee app password.\n Enter the following OTP in the app.\n' + str(otp) + '\nDon\'t share it with anyone. The OTP will expire in 10 minutes.'
            msg.attach(MIMEText(body))
            smtp = smtplib.SMTP(server, 587)

            smtp.starttls()

            smtp.login(user, user_password)

            smtp.sendmail(user, email_id, msg.as_string())

            smtp.close()

            users.sudo().write({'otp': str(otp), 'otp_time': otp_time})

            return "1"
        else:
            return "0"

    @http.route('/employee/reset_password/otp', methods=['POST'], auth='public', csrf=False)
    def get_otp_value(self, **kwargs):
        email_id = kwargs.get('email')
        otp_data = kwargs.get('otpnew')
        users = request.env['res.users'].sudo().search([('login', '=', str(email_id))])
        if users:
            otp = users.otp
            otp_time = users.otp_time
            confirm_time = datetime.datetime.now()
            otp_time_diff = confirm_time - otp_time

            seconds = otp_time_diff.seconds
            validity_time = 600
            if otp == otp_data:
                if seconds > validity_time:
                    return '0'
                else:
                    return '1'
            else:
                return '0'
        else:
            return '0'

    @http.route('/employee/reset_password/confirm', methods=['POST'], auth='public', csrf=False)
    def get_confirm_password(self, **kwargs):
        email_id = kwargs.get('email')
        new_password = kwargs.get('cpassword')


        users = request.env['res.users'].sudo().search([('login', '=', str(email_id))])

        if users:
            users.sudo().write({'password': new_password})
            return '1'
        else:
            return '0'


class reset_password_customer(http.Controller):

    @http.route('/reset_password/customer', methods=['POST'], auth='public', csrf=False)
    def get_email_id(self, **kwargs):
        email_id = kwargs.get('email')
        users = request.env['res.users'].sudo().search([('login', '=', str(email_id))])

        if users and users.customer is True:

            otp = random.randint(1000, 9999)
            otp_time = datetime.datetime.now()
            user_name = users.name

            mail = request.env['ir.mail_server'].sudo().search([], limit=1)
            user = mail.smtp_user
            user_password = mail.smtp_pass
            server = mail.smtp_host
            msg = MIMEMultipart()
            msg['From'] = user
            msg['To'] = email_id
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = str(otp) + ' is your PureCannabis app password recovery code '
            body = 'Hi ' + user_name + ',\n\n We received a request to reset your Purecannabis app password.\n Enter the following OTP in the app.\n' + str(otp) + '\nDon\'t share it with anyone. The OTP will expire in 10 minutes.'
            msg.attach(MIMEText(body))
            smtp = smtplib.SMTP(server, 587)
            smtp.starttls()
            smtp.login(user, user_password)
            smtp.sendmail(user, email_id, msg.as_string())
            smtp.close()
            users.sudo().write({'otp': str(otp), 'otp_time': otp_time})
            return "1"
        else:
            return "0"

    @http.route('/reset_password/customer/otp', methods=['POST'], auth='public', csrf=False)
    def get_otp_value(self, **kwargs):

        email_id = kwargs.get('email')
        otp_data = kwargs.get('otpnew')
        users = request.env['res.users'].sudo().search([('login', '=', str(email_id))])
        if users:
            otp = users.otp
            otp_time = users.otp_time
            confirm_time = datetime.datetime.now()
            otp_time_diff = confirm_time - otp_time

            seconds = otp_time_diff.seconds
            validity_time = 600
            if otp == otp_data:
                if seconds > validity_time:
                    return '0'
                else:
                    return '1'
            else:
                return '0'
        else:
            return '0'

    @http.route('/reset_password/customer/confirm', methods=['POST'], auth='public', csrf=False)
    def get_confirm_password(self, **kwargs):
        email_id = kwargs.get('email')
        new_password = kwargs.get('cpassword')

        users = request.env['res.users'].sudo().search([('login', '=', str(email_id))])
        if users:
            users.sudo().write({'password': new_password})
            return '1'
        else:
            return '0'
