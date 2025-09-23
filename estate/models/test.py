# -*- coding: utf-8 -*-
from odoo import models, fields, api

# Inheritable classes
# models.Model: For regular models
# models.AbstractModel: For abstract models meant to be inherited by some other models
# models.TransientModel: For temporary model that automatically gets deleted.
class TestModel(models.Model):
    _name = "test_model" # Name of model
    _description = "A brief description of the model"
    _inherit = "" # To inherit any previous modules.

    def _default_name(self):
        return self.get_value()

    def _search_partner_ref(self, operator, value):
        if operator not in ('in', 'like'):
            return NotImplemented
        return Domain('partner_id.ref', operator, value)

    # Simple
    field_1 = fields.Boolean()
    field_2 = fields.Char()
    field_3 = fields.Text()
    field_4 = fields.Selection()
    field_5 = fields.Float()
    field_6 = fields.Integer()
    field_7 = fields.Date()
    field_8 = fields.Datetime()
    field_9 = fields.Binary()
    field_10 = fields.HTML()
    # Relational
    field_11 = fields.Many2One()
    field_12 = fields.One2Many()
    field_13 = fields.Many2Many()


    # string: Field Name
    # invisible: Whether to show/hide in view
    # readonly: Whether field is editable or not
    # required: Whether field must have a value or not
    # default: Initialized value of field

    field1 = fields.Char()
    field2 = fields.Integer(
        string = "", # Label of field, default = Capitalized version of name
        help = "", # Tooltip for field
        required = True, # If field is compulsary
        default = "", # Default value of field when created.
        default = lambda self: self._default_name(), # When you want to calculate defalt value.
        groups = "a,b", # List of xml ids thats used to restrict access to users 
        copy = True, # Should value be copied if record is duplicated
        store = True, # Should value be stored in database (False when computed fields)
        search = "", # Name of method to implement search
        compute = "", # Name of method to auto calculate value
        related = "", # model.fieldname of a related model.
        depends = [], # recompute related value if given specific value changes.
    )

    field3 = fields.ManyToOne(
        comodel_name = "", # Name of related model,
    )

    field3 = fields.OneToMany(
        comodel_name = "", # Name of related model,
        inverse_name = "", # Name of ManyToOne field in related Model
    )

    @api.depends('value','tax') # value and tax part of same model.
    def _compute_total(self):
        for record in self:
            record.total = value + (value * tax)

    @api.depends('related_ids.value') # value from oneToMany relation of other model
    def _compute_total_2(self):
        for record in self:
            record.total = sum(line.value for line in record.line.ids)

