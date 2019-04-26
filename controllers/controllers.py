# -*- coding: utf-8 -*-
from odoo import http

# class Odoo-producteca(http.Controller):
#     @http.route('/odoo-producteca/odoo-producteca/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-producteca/odoo-producteca/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-producteca.listing', {
#             'root': '/odoo-producteca/odoo-producteca',
#             'objects': http.request.env['odoo-producteca.odoo-producteca'].search([]),
#         })

#     @http.route('/odoo-producteca/odoo-producteca/objects/<model("odoo-producteca.odoo-producteca"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-producteca.object', {
#             'object': obj
#         })