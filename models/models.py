# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
	_inherit = 'sale.order'

	@api.model
	def connect_producteca(self):
		raise ValidationError("Connect Producteca Test")

	integration_id = fields.Char('IntegrationId')
	doc_xml = fields.Text('XML')
