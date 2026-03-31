from odoo import models,fields

class ProductMaster(models.Model):
    _name="Product Specification Sheet"
    _description="Contains complete details related to printing given product label"

    product_code=fields.Char()
    description=fields.Char()
    customer=fields.Many2One()
    sales_order=fields.Many2One()
    artwork_id=fields.Char(
        related="artwork_master.art_id"
    )
    new_artwork=fields.Boolean() # When new/updated artwork, becomes true, later on SO approval, becomes false.
    extra_quantity_allowed=fields.Integer()
    rolls=fields.Integer()
    carton_size=fields.Char()


