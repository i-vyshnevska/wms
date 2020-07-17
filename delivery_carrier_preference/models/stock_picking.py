# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"

    estimated_shipping_weight = fields.Float(
        string="Estimated shipping weight (kg)",
        compute="_compute_estimated_shipping_weight",
        help="This weight is calculated according to the move quantity and"
        " existing product packagings weight for each product on the "
        "moves.",
    )

    @api.depends("move_lines", "move_lines.estimated_shipping_weight")
    def _compute_estimated_shipping_weight(self):
        for pick in self:
            pick.estimated_shipping_weight = sum(
                pick.move_lines.mapped("estimated_shipping_weight")
            )

    def get_preferred_carrier(self):
        self.ensure_one()
        return fields.first(
            self.env[
                "delivery.carrier.preference"
                # TODO Apply carrier preference domain here?
            ].get_preferred_carriers(
                self.partner_id, self.estimated_shipping_weight, self.company_id
            )
        )

    def add_preferred_carrier(self):
        self.ensure_one()
        carrier = self.get_preferred_carrier()
        if not carrier:
            return {
                "warning": {
                    "title": _("Cannot find preferred carrier"),
                    "message": _(
                        "No preferred carrier could be found "
                        "automatically for this delivery order. Please"
                        "select one manually."
                    ),
                }
            }
        else:
            self.carrier_id = carrier
