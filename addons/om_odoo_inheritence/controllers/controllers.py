# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/extra-addons/omOdooInheritence(http.Controller):
#     @http.route('//mnt/extra-addons/om_odoo_inheritence//mnt/extra-addons/om_odoo_inheritence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/om_odoo_inheritence//mnt/extra-addons/om_odoo_inheritence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/om_odoo_inheritence.listing', {
#             'root': '//mnt/extra-addons/om_odoo_inheritence//mnt/extra-addons/om_odoo_inheritence',
#             'objects': http.request.env['/mnt/extra-addons/om_odoo_inheritence./mnt/extra-addons/om_odoo_inheritence'].search([]),
#         })

#     @http.route('//mnt/extra-addons/om_odoo_inheritence//mnt/extra-addons/om_odoo_inheritence/objects/<model("/mnt/extra-addons/om_odoo_inheritence./mnt/extra-addons/om_odoo_inheritence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/om_odoo_inheritence.object', {
#             'object': obj
#         })
