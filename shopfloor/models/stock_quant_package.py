from odoo import fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    moved_move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        inverse_name="package_id",
        readonly=True,
        help="Technical field. Move lines for which source is this package.",
    )
    planned_move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        inverse_name="result_package_id",
        readonly=True,
        help="Technical field. Move lines for which destination is this package.",
    )
