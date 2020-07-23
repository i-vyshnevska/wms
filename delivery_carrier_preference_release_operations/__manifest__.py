# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Delivery Carrier Preference Release Operations",
    "summary": "Trigger recomputation of preferred carrier on release of operations",
    "version": "13.0.1.2.0",
    "category": "Operations/Inventory/Delivery",
    "website": "https://github.com/OCA/delivery-carrier",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "delivery_carrier_preference",
        "stock_available_to_promise_release",
        "stock_picking_group_by_partner_by_carrier",
    ],
    "data": ["views/stock_picking_type.xml"],
}
