# -*- coding: utf-8 -*-
# from odoo import http


# class Horoof(http.Controller):
#     @http.route('/horoof/horoof', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/horoof/horoof/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('horoof.listing', {
#             'root': '/horoof/horoof',
#             'objects': http.request.env['horoof.horoof'].search([]),
#         })

#     @http.route('/horoof/horoof/objects/<model("horoof.horoof"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('horoof.object', {
#             'object': obj
#         })
