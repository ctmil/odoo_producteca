# -*- coding: utf-8 -*-

from odoo import models, fields, api

class odoo-producteca(models.Model):
	_inherit = 'sale.order'

	integration_id = fields.Char('IntegrationId')
	doc_xml = fields.Text('XML')
