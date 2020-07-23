# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class StockMove(models.Model):

    _inherit = "stock.move"

    def release_available_to_promise(self):
        existing_backorders = {
            pick.id: pick.mapped("backorder_ids").ids
            for pick in self.mapped("picking_id")
        }
        res = super().release_available_to_promise()
        for picking in self.mapped("picking_id"):
            pick_type = picking.picking_type_id
            if (
                picking.picking_type_code != "outgoing"
                or not pick_type.force_recompute_preferred_carrier_on_release
            ):
                continue
            original_carrier = picking.carrier_id
            picking.add_preferred_carrier()
            if original_carrier != picking.carrier_id:
                new_backorder = picking.backorder_ids.filtered(
                    lambda b: b.id not in existing_backorders.get(picking.id)
                )
                if new_backorder:
                    new_proc_group = picking.group_id.copy()
                    new_backorder.group_id = new_proc_group
                    new_backorder.move_lines.write({"group_id": new_proc_group.id})
                picking.group_id.carrier_id = picking.carrier_id
        return res
