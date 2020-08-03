# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.osv.expression import AND
from odoo.tools.safe_eval import const_eval


class StockPicking(models.Model):

    _inherit = "stock.picking"

    estimated_shipping_weight = fields.Float(
        string="Estimated shipping weight",
        compute="_compute_estimated_shipping_weight",
        help="This weight is calculated according to the move quantity "
        "available to promise and existing product packagings weight for each "
        "product on the moves.",
    )

    @api.depends("move_lines", "move_lines.estimated_shipping_weight")
    def _compute_estimated_shipping_weight(self):
        for pick in self:
            pick.estimated_shipping_weight = sum(
                pick.move_lines.mapped("estimated_shipping_weight")
            )

    def add_preferred_carrier(self):
        self.ensure_one()
        carrier = fields.first(self.get_preferred_carriers())
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

    def get_preferred_carriers(self):
        # TODO Check possible conflicting settings between doc company and
        #  user preference defined on another company?
        self.ensure_one()
        company_carriers = self.env["delivery.carrier"].search(
            ["|", ("company_id", "=", False), ("company_id", "=", self.company.id)]
        )
        carrier_preferences = self.env["delivery.carrier.preference"].search(
            [
                "&",
                "|",
                ("max_weight", ">=", self.estimated_shipping_weight),
                ("max_weight", "=", 0.0),
                "|",
                ("carrier_id", "in", company_carriers.ids),
                ("carrier_id", "=", False),
            ]
        )
        carriers_ids = list()
        for cp in carrier_preferences:
            if cp.picking_domain and not self._is_valid_delivery_preference(cp):
                continue
            if cp.preference == "carrier":
                carriers_ids.append(cp.carrier_id.id)
            else:
                partner_carrier = self.partner_id.property_delivery_carrier_id
                if partner_carrier:
                    carriers_ids.append(partner_carrier.id)
        return (
            self.env["delivery.carrier"]
            .browse(carriers_ids)
            .available_carriers(self.partner_id)
        )

    def _is_valid_delivery_preference(self):
        self.ensure_one()
        domain = const_eval(self.picking_domain)
        if not domain:
            return True
        else:
            return self.env["stock.picking"].search_count(
                AND(domain, [("id", "=", self.id)])
            )
