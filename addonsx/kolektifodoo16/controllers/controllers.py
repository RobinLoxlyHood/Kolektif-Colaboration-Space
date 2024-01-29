# -*- coding: utf-8 -*-
# from odoo import http


# class Kolektif(http.Controller):
#     @http.route('/kolektif/kolektif', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kolektif/kolektif/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kolektif.listing', {
#             'root': '/kolektif/kolektif',
#             'objects': http.request.env['kolektif.kolektif'].search([]),
#         })

#     @http.route('/kolektif/kolektif/objects/<model("kolektif.kolektif"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kolektif.object', {
#             'object': obj
#         })
