from odoo import fields, models, api, _


# class BoM(models.Model):
#     _name = 'bom'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#
#     _description = 'Bill of Material'
#
#     name = fields.Char(string='Order Reference', required=True,
#                        readonly=True, default=lambda self: _('New'))
#     product_id = fields.Many2one('product.product', string='Product', tracking=True)
#
#     product_variant_id = fields.Many2one('product.product', string='Product Variant',
#                                          domain="[('id', '=', product_id)]")
#     quantity = fields.Integer(string='Quantity', default='1', tracking=True)
#     uom = fields.Many2one('uom.uom', string='Units')
#     reference = fields.Char(string='Reference')
#     company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, tracking=True)
#     #########################################
#     order_line_product_ids = fields.One2many('product.info', 'line_product_id')
#     product_name_ids = fields.One2many('product.info', 'product_name_id')
#     description_id = fields.Char(string='Description')
#     toconsume = fields.Integer(string='To Consume')
#
#     @api.model
#     def create(self, vals):
#         if vals.get('name', _('New')) == _('New'):
#             vals['name'] = self.env['ir.sequence'].next_by_code(
#                 'bom')
#         res = super(BoM, self).create(vals)
#         return res
#
#     @api.onchange('product_id')
#     def auotoload_uom(self):
#         if self.product_id:
#             self.uom = self.product_id.uom_id
