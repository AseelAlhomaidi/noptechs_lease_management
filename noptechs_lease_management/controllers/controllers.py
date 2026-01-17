# from odoo import http


# class NoptechsLeaseManagement(http.Controller):
#     @http.route('/noptechs_lease_management/noptechs_lease_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/noptechs_lease_management/noptechs_lease_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('noptechs_lease_management.listing', {
#             'root': '/noptechs_lease_management/noptechs_lease_management',
#             'objects': http.request.env['noptechs_lease_management.noptechs_lease_management'].search([]),
#         })

#     @http.route('/noptechs_lease_management/noptechs_lease_management/objects/<model("noptechs_lease_management.noptechs_lease_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('noptechs_lease_management.object', {
#             'object': obj
#         })

