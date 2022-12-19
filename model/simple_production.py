from odoo import fields, models, api, _


class SimpleProduction(models.Model):
    _name = 'simple.production'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'A Simple Production App'

    name = fields.Char(string='Order Reference', required=True, readonly=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.product', string='Product', tracking=True, required=True)
    quantity = fields.Float(string='Quantity', default='1', tracking=True)
    uom = fields.Char(string='Units', readonly=True)
    bill_of_material = fields.Many2one('mrp.bom', 'Bill of Material', states={'draft': [('readonly', False)]},
                                       check_company=True,
                                       domain="[('product_tmpl_id.product_variant_ids', '=', product_id)]",
                                       help="Bill of Materials allow you to define the list of required components to "
                                            "make a finished product.")

    scheduled_date = fields.Datetime(string='Date', default=fields.Datetime.now())
    responsible_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True)
    status = fields.Selection(string='Status', copy=False,
                              selection=[('draft', 'Draft'), ('confirmed', 'Confirmed'),
                                         ('done', 'Done'), ('cancel', 'Cancel')], default='draft', tracking=True)
    ################################
    simple_product_line_ids = fields.One2many('simpleproduct.info', 'simple_product_line_id')
    product_line_name_ids = fields.One2many('simpleproduct.info', 'product_line_name_id')
    description_id = fields.Char(string='Description')
    toconsume = fields.Integer(string='To Consume')
    ################################
    original_qty = fields.Float(related='bill_of_material.product_qty')
    ratio = fields.Integer()
    flag = fields.Integer()

    @api.onchange('bill_of_material')
    def onchange_product(self):
        print("FDRFEDREGFDCREFDREFD")
        print(self.bill_of_material.id)
        print(self.bill_of_material.product_tmpl_id.id)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'simple.production')
        res = super(SimpleProduction, self).create(vals)
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):

        bom = self.env['mrp.bom']._bom_find(self.product_id, company_id=self.company_id.id, )[self.product_id]
        print(bom)
        print(bom.id)
        if bom:
            self.bill_of_material = bom.id
            self.quantity = bom.product_qty
            self.uom = self.product_id.uom_id.name
            for rec in self:
                print(self)
                components = [(5, 0, 0)]
                print("self.bill_of_material", self.bill_of_material.bom_line_ids)
                for i in self.bill_of_material.bom_line_ids:
                    vals = {
                        'product_line_name_id': i.product_id,
                        'toconsume': i.product_qty,
                        'qty': i.product_qty,
                    }
                    components.append((0, 0, vals))
                print("components", components)
                rec.simple_product_line_ids = components

        else:
            self.bill_of_material = False
            self.quantity = 1
            self.simple_product_line_ids = False
            self.uom = self.product_id.uom_id.name

    @api.onchange('quantity')
    def update_toconsume(self):
        if self.bill_of_material:
            o_qty = int(self.original_qty)
            self.ratio = self.quantity / o_qty
            for rec in self.simple_product_line_ids:
                rec.toconsume = rec.qty * self.ratio

    def button_confirmed(self):
        self.status = 'confirmed'
        print("confirmed")

    def button_mark_as_done(self):
        self.status = 'done'
        print("done")
        print(self.product_id.id)
        dest_location = self.env['stock.location'].search(
            [('usage', '=', 'internal',), ('name', '=', 'Stock'), ('company_id', '=', self.company_id.id)])
        print("fewxweradskdwjsahesa",dest_location)
        src_location = self.env['stock.location'].search(
            [('usage', '=', 'production'),  ('company_id', '=', self.company_id.id)])

        move = self.env['stock.move'].create({
            'name': 'Use on MyLocation',
            'location_id': src_location.id,
            'location_dest_id': dest_location.id,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_id.id,
            'product_uom_qty': self.quantity,
        })
        move._action_confirm()
        move._action_assign()
        move.move_line_ids.write({
            'qty_done': self.quantity})
        # This creates a stock.move.line record. You could also do it manually
        move._action_done()
        if self.simple_product_line_ids:
            for product in self.simple_product_line_ids:
                print("#############")
                print(product.product_line_name_id.id)
                print(product.product_line_name_id.product_tmpl_id)
                print(product.product_line_name_id.product_tmpl_id.name)
                move1 = self.env['stock.move'].create({
                    'name': 'Use on MyLocation',
                    'location_id': dest_location.id,
                    'location_dest_id': src_location.id,
                    'product_id': product.product_line_name_id.id,
                    'product_uom': product.product_line_name_id.uom_id.id,
                    'product_uom_qty': product.toconsume,
                })
                move1._action_confirm()
                move1._action_assign()
                # This creates a stock.move.line record. You could also do it manually
                move1.move_line_ids.write({'qty_done': (product.toconsume)})
                move1._action_done()
                print(product.product_line_name_id.id, "product id")
                print(product.product_line_name_id.uom_id.id, "uom id")
                print(product.toconsume, "quantity")

    def button_cancel(self):
        self.status = 'cancel'
