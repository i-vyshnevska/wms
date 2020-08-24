# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.shopfloor.tests.test_location_content_transfer_mix import (
    LocationContentTransferMixCase,
)


class LocationContentTransferZonePickingCase(LocationContentTransferMixCase):
    """Tests where we mix location content transfer with other scenarios."""

    def test_with_zone_picking(self):
        """Test the following scenario:

        1) An operator processes the first pallet with the "zone picking" scenario
           to move the goods to PACK-1:

            move1 PICK -> PACK-1 'done'

        2) At this point, every PICK sibling move lines should now target PACK-1
        """
        move_lines = self.picking1.move_line_ids
        pick_move_line1 = move_lines[0]
        pick_move_line2 = move_lines[1]
        # The operator process the first pallet with the "zone picking" scenario
        orig_dest_location = pick_move_line2.location_dest_id
        dest_location = pick_move_line2.location_dest_id.sudo().copy(
            {
                "name": orig_dest_location.name + "_1",
                "barcode": orig_dest_location.barcode + "_1",
                "location_id": orig_dest_location.id,
            }
        )
        self._zone_picking_process_line(pick_move_line1, dest_location=dest_location)
        # __import__("pdb").set_trace()
        # At this point, all PICK move lines should share the same destination
        # and the PACK moves has this location as source
        __import__("pdb").set_trace()
        self.assertEqual(self.pack_move_a.location_id, dest_location)
        self.assertEqual(pick_move_line1.location_dest_id, dest_location)
        self.assertEqual(pick_move_line2.location_dest_id, dest_location)
        self.assertEqual(pick_move_line1.move_id.location_dest_id, dest_location)
        self.assertEqual(pick_move_line2.move_id.location_dest_id, dest_location)
