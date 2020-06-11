# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Stock Storage Type",
    "summary": "Manage packages and locations storage types",
    "version": "13.0.1.0.0",
    "development_status": "Alpha",
    "category": "Warehouse Management",
    "website": "https://github.com/OCA/wms",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base_m2m_custom_field",
        "stock_quant_package_dimension",
        "web_domain_field",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_packaging.xml",
        "views/stock_location.xml",
        "views/stock_location_package_storage_type_rel.xml",
        "views/stock_location_storage_type.xml",
        "views/stock_package_level.xml",
        "views/stock_package_storage_type.xml",
        "views/stock_quant_package.xml",
        "views/stock_storage_location_sequence.xml",
        "views/storage_type_menus.xml",
    ],
    "demo": [
        "demo/stock_location_storage_type.xml",
        "demo/stock_package_storage_type.xml",
        "demo/product_packaging.xml",
        "demo/stock_location.xml",
        "demo/stock_storage_location_sequence.xml",
    ],
}
