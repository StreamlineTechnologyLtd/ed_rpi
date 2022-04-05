# -*- coding: utf-8 -*-
# from odoo import http


# class Rpi(http.Controller):
#     @http.route('/rpi/rpi', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rpi/rpi/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rpi.listing', {
#             'root': '/rpi/rpi',
#             'objects': http.request.env['rpi.rpi'].search([]),
#         })

#     @http.route('/rpi/rpi/objects/<model("rpi.rpi"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rpi.object', {
#             'object': obj
#         })
