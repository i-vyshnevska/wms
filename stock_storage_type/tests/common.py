# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SavepointCase


class TestStorageTypeCommon(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        ref = cls.env.ref
        cls.warehouse = ref("stock.warehouse0")
        # set two steps reception on warehouse
        cls.warehouse.reception_steps = "two_steps"

        cls.suppliers_location = ref("stock.stock_location_suppliers")
        cls.input_location = ref("stock.stock_location_company")
        cls.stock_location = ref("stock.stock_location_stock")

        cls.cardboxes_location = ref("stock_storage_type.stock_location_cardboxes")
        cls.pallets_location = ref("stock_storage_type.stock_location_pallets")
        cls.pallets_reserve_location = ref(
            "stock_storage_type.stock_location_pallets_reserve"
        )
        cls.areas = (
            cls.cardboxes_location | cls.pallets_location | cls.pallets_reserve_location
        )
        # cls.putaway_locations = cls.cardboxes_location | cls.pallets_location

        cls.cardboxes_bin_1_location = ref(
            "stock_storage_type.stock_location_cardboxes_bin_1"
        )
        cls.cardboxes_bin_2_location = ref(
            "stock_storage_type.stock_location_cardboxes_bin_2"
        )
        cls.cardboxes_bin_3_location = ref(
            "stock_storage_type.stock_location_cardboxes_bin_3"
        )
        cls.cardboxes_bin_4_location = cls.cardboxes_bin_1_location.copy(
            {"name": "Bin 4"}
        )
        cls.env['stock.location']._parent_store_compute()
        cls.pallets_bin_1_location = ref(
            "stock_storage_type.stock_location_pallets_bin_1"
        )
        cls.pallets_bin_2_location = ref(
            "stock_storage_type.stock_location_pallets_bin_2"
        )
        cls.pallets_bin_3_location = ref(
            "stock_storage_type.stock_location_pallets_bin_3"
        )

        cls.receipts_picking_type = ref("stock.picking_type_in")
        cls.internal_picking_type = ref("stock.picking_type_internal")

        cls.product = ref("product.product_product_9")
        cls.product_lot = ref("stock.product_cable_management_box")

        cls.cardboxes_package_storage_type = ref(
            "stock_storage_type.package_storage_type_cardboxes"
        )
        cls.pallets_package_storage_type = ref(
            "stock_storage_type.package_storage_type_pallets"
        )
        cls.cardboxes_location_storage_type = ref(
            "stock_storage_type.location_storage_type_cardboxes"
        )
        cls.pallets_location_storage_type = ref(
            "stock_storage_type.location_storage_type_pallets"
        )

        cls.product_cardbox_product_packaging = ref(
            "stock_storage_type." "product_product_9_packaging_4_cardbox"
        )
        cls.product_pallet_product_packaging = ref(
            "stock_storage_type." "product_product_9_packaging_48_pallet"
        )
        cls.product_lot_cardbox_product_packaging = cls.env["product.packaging"].create(
            {
                "name": "5 units cardbox",
                "qty": 5,
                "product_id": cls.product_lot.id,
                "package_storage_type_id": cls.cardboxes_package_storage_type.id,
            }
        )
        cls.product_lot_pallets_product_packaging = cls.env["product.packaging"].create(
            {
                "name": "20 units pallet",
                "qty": 20,
                "product_id": cls.product_lot.id,
                "package_storage_type_id": cls.pallets_package_storage_type.id,
            }
        )
        cls.internal_picking_type.write({'show_entire_packs': True})
        # show_reserved must be set here because it changes the behaviour of
        # put_in_pack operation:
        # if show_reserved: qty_done must be set on stock.picking.move_line_ids
        # if not show_reserved: qty_done must be set on stock.picking.move_line_nosuggest_ids
        cls.receipts_picking_type.write({'show_entire_packs': True, 'show_reserved': True})
