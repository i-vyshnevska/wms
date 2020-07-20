# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class StockMove(models.Model):

    _inherit = "stock.move"

    def release_available_to_promise(self):
        res = super().release_available_to_promise()
        for picking in self.mapped("picking_id"):
            pick_type = picking.picking_type_id
            if (
                picking.picking_type_code != "outgoing"
                or not pick_type.force_recompute_preferred_carrier_on_release
            ):
                continue
            picking.add_preferred_carrier()
        return res
