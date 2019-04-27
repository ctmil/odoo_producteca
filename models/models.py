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

				user = self.env['res.partner'].search([('ref', '=', ref)])

				if not user:
					#raise ValidationError("!")
					#create partner
					self.env['res.partner'].create({
						'name': name,
						'ref': ref,
						'email': email,
						'phone': phone,
						'street': street,
						'street2': street2,
						'city': city,
						'zip': zip
					})
					self.env.cr.commit()

				raise ValidationError(name + " Test")

	integration_id = fields.Char('IntegrationId')
	doc_xml = fields.Text('XML')
