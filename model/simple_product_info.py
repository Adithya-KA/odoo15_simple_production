from odoo import fields, models


class ProductInfoSimpleProduct(models.Model):
    _name = 'simpleproduct.info'

    simple_product_line_id = fields.Many2one('simple.production')
    product_line_name_id = fields.Many2one('product.product')
    description_id = fields.Char(string='Description', related='product_line_name_id.name', readonly=True)
    toconsume = fields.Integer(string='To Consume')
    qty = fields.Integer('Quantity')
