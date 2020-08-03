# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    estimated_shipping_weight = fields.Float(
        string="Estimated shipping weight",
        compute="_compute_estimated_shipping_weight",
        help="Total weight calculated according to the move quantity and "
        "weight defined on packagings for this product.",
    )

    @api.depends(
        "product_id",
        "product_id.packaging_ids",
        "product_id.packaging_ids.max_weight",
        "product_id.weight",
    )
    def _compute_estimated_shipping_weight(self):
        for move in self:
            prod = move.product_id
            move.estimated_shipping_weight = prod.get_total_weight_from_packaging(
                move.product_qty
            )
