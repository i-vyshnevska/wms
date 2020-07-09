# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class StockLocationStorageBuffer(models.Model):
    _name = "stock.location.storage.buffer"
    _description = "Location Storage Buffer"

    buffer_location_ids = fields.Many2many(
        comodel_name="stock.location",
    )
    bin_location_ids = fields.Many2many(
        comodel_name="stock.location",
    )
    # add computed field for children?


    # TODO override stocklocation.select_allowed_locations?
    # use buffer_location_ids.location_is_empty
