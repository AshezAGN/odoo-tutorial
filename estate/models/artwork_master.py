from odoo import models,fields

class LabelArtwork(models.Model):
    _name="artwork_master"
    _description="Contains list of approved artwork"

    art_id = fields.Char(
        string='Artwork Code',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default='New'
    )
    title = fields.Char(
        string="Title",
    )
    file = fields.Binary(
        string="Attachment",
        attachment=True,
        help="Upload the approved artwork here"
    )
    die_code = fields.Many2One(
        string = "Die Cutter",
        required=True,
        comodel_name="die_master",
        relation="die_master.die_code"
    )
    customer = fields.Many2One(
        string="Customer",
        required=True,
        # comodel_name=""
    )
    no_of_colors = fields.Integer(
        string="Number of colors",
        required=True,
    )
    uv_varnish = fields.Selection(
        string="UV Varnish",
        selection=[
            ("matt","Matt"),
            ("gloss","Gloss"),
            ("spot_gloss","Spot Gloss"),
            ("none","None")
        ],
        default="none"
    )
    cold_foil = fields.Selection(
        string="Foil",
        selection=[
            ("silver","Silver"),
            ("gold","Gold"),
            ("color","Color"),
            ("none","None")
        ],
        default="none"
    )
    lamination = fields.Boolean(
        string="Lamination",
        default=False
    )
    uv_primer = fields.Boolean(
        string="UV Primer",
        default=False
    )
    # REDO to get radio selection with images
    winding_front = fields.Selection(
        string="Winding Front Label",
        selection=[
            ("1","1"),
            ("2","2"),
            ("3","3"),
            ("4","4"),
            ("5","5"),
            ("6","6"),
            ("7","7"),
            ("8","8"),
        ]
    )
    winding_back = fields.Integer(
        string="Winding Back Label",
        selection=[
            ("0","None")
            ("1","1"),
            ("2","2"),
            ("3","3"),
            ("4","4"),
            ("5","5"),
            ("6","6"),
            ("7","7"),
            ("8","8"),
        ]
    )
    lsd_number = fields.Integer(
        string="LSD Number"
    )
    barcode = fields.Integer(
        string="Barcode"
    )
    core = fields.Integer(
        string="Core"
    )
    labels_per_core = fields.Integer(
        string="Labels per core"
    )

@api.model
    def create(self, vals):
        # When record is created, update id to the next sequence.
        if vals.get('id', 'New') == 'New':
            vals['id'] = self.env['ir.sequence'].next_by_code('diecutter.seq') or 'New'
        return super(LabelArtwork, self).create(vals)
