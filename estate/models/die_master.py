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
    around_ups = fields.Integer(
        string="Around Ups",
        # computed=""
    )
    around_gaps = fields.Float(
        string="Around Gaps (mm)",
        # computed=""
    )
    # total_ups = fields.Integer()
    magnetic_cylinder = fields.Integer(
        string="Magnetic Cylinder (T)",
        # computed=""
    )
    die_option = fields.Many2One(
        string="Die Option",
        required=True,
        comodel_name="die_options",
        relation="die_options.name"
    )
    face_stock = fields.Many2One(
        string="Face Stock",
        required=True,
        comodel_name="face_stocks",
        relation="face_stocks.name"
    )
    liner = fields.Many2One(
        string="Liner",
        required=True,
        comodel_name="liners",
        relation="liners.name"
    )

    @api.model
    def create(self, vals):
        # When record is created, update id to the next sequence.
        if vals.get('die_code', 'New') == 'New':
            vals['die_code'] = self.env['ir.sequence'].next_by_code('diecutter.seq') or 'New'
        return super(DieCutter, self).create(vals)

    def calculate_all_around_gaps(teeths):
        for teeth in all_teeth:
            teeth.around_ups = math.floor(teeth.cylinder_teeth / (record.repeat_length * 2.5))
            teeth.around_gaps = (cylinder_repeat / teeth.around_ups) + record.repeat_length
        return sorted(all_teeth, key=lambda t: t.around_gaps)

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
                sorted_teeths = calculate_all_around_gaps(all_teeth)
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
                record.around_ups = math.floor(record.cylinder_repeat / (record.repeat_length * 2.5))
                record.around_gaps = (record.cylinder_repeat / record.around_ups) + record.repeat_length
                record.total_ups = record.around_ups * record.around_gaps
                # Calculate cylinder teeths above 72 having same around gap value as this.
                if record.cylinder_teeth in [64,67,72]:
                    sorted_teeths = calculate_all_around_gaps(all_teeth)
                    for teeth in sorted_teeth:
                        if teeth.cylinder_repeat not in [64,67,72] and teeth.around_gaps == record.around_gaps:
                            record.magnetic_cylinder = teeth.cylinder_repeat
                            break
                    else:
                        magnetic_cylinder = 0  
                # Same as cylinder teeth when below 73  
                else:
                    record.magnetic_cylinder = record.cylinder_teeth



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
