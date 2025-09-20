from odoo import models
import math

class DieMaster(models.Model):
    _name = "die_master"
    _description = "A set of die cutters used in print job"

    die_code = fields.Char(
        string='Die Code',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default='New'
    )
    die_type = fields.Many2One(
        string="Die Type",
        required=True,
        comodel_name="die_types",
        relation="die_types.name"
    )
    width_across = fields.Integer(
        string="Width Across (mm)",
        required=True,
    )
    repeat_length = fields.Integer(
        string="Repeat Length (mm)",
        required=True,
    )
    corner_radius = fields.Integer(
        string="Radius (mm)",
        required=True,
    )
    across_ups = fields.Integer(
        string="Across Ups",
        required=true,
        # computed = ""
    )
    across_gaps = fields.Integer(
        string="Across Gaps",
        required=true,
        # computed = ""
    )
    cylinder_teeth = fields.Many2One(
        domain='[]',
        # comodel_name='cylinder_master',
        # relation='cylidner_master.cylinder_teeth'
    )
    cylinder_repeat = fields.Float(
        string="Cylinder Repeat (mm)"
        computed="_compute_cylinder_repeat"
    )
    around_ups = fields.Integer()
    around_gaps = fields.Float()
    total_ups = fields.Integer()
    magnetic_cylinder = fields.Integer()
    die_option = fields.Many2One()
    face_stock = fields.Many2One()
    liner = fields.Many2One()
    # die_status = fields.Selection()

    @api.model
    def create(self, vals):
        # When record is created, update id to the next sequence.
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('diecutter.seq') or 'New'
        return super(DieCutter, self).create(vals)

    # Updates each time repeat_length changes
    @api.onchange("repeat_length")
    def _onchange_get_recommended_teeth(self):
        # When repeat_length is inputted, suggest 6 best cylinder teeth that best work for it.
        for record in self:
            if not rec.repeat_length:
                return {
                    'domain': {'cylinder_teeth': []}
                }
            else:
                all_teeth = self.env['cylinder.teeth'].search([])
                # Calculate around ups and around gaps.
                for teeth in all_teeth:
                    teeth.around_ups = math.floor(teeth.cylinder_teeth / (record.repeat_length * 2.5))
                    teeth.around_gaps = (cylinder_repeat / teeth.around_ups) + record.repeat_length
                sorted_teeths = sorted(all_teeth, key=lambda t: t.around_gaps)
                # Get 6 unique smallest values.
                seen = set()
                unique_teeths = []
                for teeth in sorted_teeth:
                    if teeth.aroud_gaps not in seen:
                        unique_teeths.append(teeth.cylinder_teeth)
                    if len(unique_teeths) >= 6:
                        break
                return {
                    # 'id' ?
                    'domain': {'cylinder_teeth': [('id','in',unique_teeths)]}
                }

    @api.depends('cylinder_teeth')
    def _compute_cylinder_repeat(self):
        for record in self:
            if record.cylinder_teeth:
                record.cylinder_repeat = 3.125 * record.cylinder_teeth


class CylinderTeeth(models.Model):
    _name = 'cylinder.teeth'
    _description = 'Cylinder Teeth Master'

    cylinder_teeth = fields.Integer(required=True)
    cylinder_repeat = fields.Integer("Cyliner Repeat (mm)", required=True)

class DieType(models.Model):
    _name = "die_types"
    _description = "Store different shape of die cutter for die type selection"

    name = fields.Char(required = true)
    die_cutter = fields.One2Many(
        comodel_name="die_master",
        inverse_name="die_type"
    )

class DieOptions(models.Model):
    _name = "die_options"

    name = fields.Char(required = true)
    die_cutter = fields.One2Many(
        comodel_name="die_master",
        inverse_name="die_option"
    )
