# from odoo import models, fields, api


# class noptechs_lease_management(models.Model):
#     _name = 'noptechs_lease_management.noptechs_lease_management'
#     _description = 'noptechs_lease_management.noptechs_lease_management'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

