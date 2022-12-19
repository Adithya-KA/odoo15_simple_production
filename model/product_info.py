# from odoo import fields, models
#
#
# class ProductInfo(models.Model):
#     _name = 'product.info'
#
#     line_product_id = fields.Many2one('bom')
#     product_name_id = fields.Many2one('product.product')
#     description_id = fields.Char(string='Description', related='product_name_id.name')
#     toconsume = fields.Integer(string='To Consume')
#     qty = fields.Integer('Quantity')
