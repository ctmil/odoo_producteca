# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	@api.model
	def connect_producteca(self):
		producteca_path =  self.env['ir.config_parameter'].search([('key', '=', 'producteca.path')]).value

		files = os.listdir(producteca_path)

		for order in files:
			f = open(producteca_path + order, 'r')
			tree = ET.parse(producteca_path + order)
			root = tree.getroot()

			for child in root:
				contact = child.find('Contact')

				ref = contact.find('Name').text
				name = contact.find('ContactPerson').text
				email = contact.find('Mail').text
				phone = contact.find('PhoneNumber').text
				street = contact.find('Location').find('StreetName').text
				street2 = contact.find('Location').find('StreetNumber').text
				state_id = contact.find('Location').find('State').text
				city = contact.find('Location').find('City').text
				zip = contact.find('Location').find('ZipCode').text
				dni = ''
				for billinginfo in root.iter('BillingInfo'):
				        dni = billinginfo.find('DocNumber').text
				user = self.env['res.partner'].search([('ref', '=', ref)])

				if not user:
					#create partner
					self.env['res.partner'].create({
						'name': name,
						'ref': ref,
						'email': email,
						'phone': phone,
						'street': street,
						'street2': street2,
						'city': city,
						'zip': zip,
						'main_id_number': dni,
						'afip_responsability_type_id': 6,
						'main_id_category_id': 35,
					})
					self.env.cr.commit()
					user = self.env['res.partner'].search([('ref', '=', ref)])
				else:
					vals = {
						'main_id_number': dni,
						'afip_responsability_type_id': 6,
						'main_id_category_id': 35,
						}
					user.write(vals)
					self.env.cr.commit()

				integration_lines = []
				for integration in root.iter('Integrations'):
					meli_integration_id = integration.find('IntegrationId').text
					integration_lines.append(meli_integration_id)

				product_lines = []
				index = 0
				for line in root.iter('Lines'):
					price = line.find('Price').text
					qty = line.find('Quantity').text
					description = line.find('Description').text
					code = line.find('Code').text
					sku = line.find('Sku').text

					product = self.env['product.product'].search([('default_code', '=', sku)])
	
					if not product:
						product = self.env['product.product'].create({
							'name': description,
							'default_code': sku,
							'list_price': price,
							'type': 'product',
							'categ_id': 1,})
					
					product_lines.append([product.id,float(price)/1.21,qty,integration_lines[index]])
					index = index + 1
				#Payment Data
				date = ''
				amount = ''
				status = ''
				method = ''
				notes = ''
				integration_id = ''

				payments = child.find('Payments').findall('Payment')
				for payment in payments:
					date = payment.find('Date').text
					amount = payment.find('Amount').text
					status = payment.find('Status').text
					method = payment.find('Method').text
					notes = payment.find('Notes').text

				InvoiceIntegration = child.find('InvoiceIntegration')
				integration_id = InvoiceIntegration.find('IntegrationId').text
				
				order_id = self.env['sale.order'].search([('integration_id', '=', integration_id)])
				if not order_id:
					order_id = self.env['sale.order'].create({
                                		'partner_id': user.id,
						'integration_id': integration_id,
						'doc_xml': f.read()
					})
				for product_line in product_lines:
					order_line = self.env['sale.order.line'].search([('meli_integration_id','=',product_line[3]),('order_id','=',order_id.id)])
					if not order_line:
						self.env['sale.order.line'].create({
							'order_id': order_id.id,
							'product_id': product_line[0],
							'product_uom_qty': product_line[2],
							'meli_integration_id': product_line[3],
							'price_unit': product_line[1]})

	integration_id = fields.Char('IntegrationId')
	doc_xml = fields.Text('XML')

class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	meli_integration_id = fields.Char('Integration ID ML')

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	@api.multi
	def _compute_integration_id(self):
		for rec in self:
			if rec.origin:
				order = self.env['sale.order'].search([('name','=',rec.origin)],limit=1)
				if order and order.integration_id:
					rec.integration_id = order.integration_id

	integration_id = fields.Char('ML Integration ID',compute=_compute_integration_id)
