# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models


class StockPackageStorageType(models.Model):

    _inherit = 'stock.package.storage.type'

    storage_location_sequence_ids = fields.One2many(
        'stock.storage.location.sequence',
        'package_storage_type_id',
        string='Storage locations sequence',
    )
    storage_type_message = fields.Html(
        compute='_compute_storage_type_message'
    )

    @api.depends('storage_location_sequence_ids')
    def _compute_storage_type_message(self):
        for pst in self:
            storage_locations = pst.storage_location_sequence_ids
            if storage_locations:
                msg = _(
                    "When a package with storage type %s is put away, the "
                    "strategy will look for an allowed location in the "
                    "following locations (as long as these locations are "
                    "children of the stock move destination location or as "
                    "long as these locations are children of the destination "
                    "location after the (product or category) putaway is "
                    "applied): %s"
                ) % (
                    pst.name, '\n'.join(
                        [
                            sl._format_package_storage_type_message()
                            for sl in storage_locations
                        ]
                    )
                )
            else:
                msg = _(
                    "The 'Storage locations sequence' must be defined in "
                    "order to put away packages using this package storage "
                    "type (%s)."
                ) % pst.name
            pst.storage_type_message = msg

    def action_view_storage_locations(self):
        return {
            'name': _('Storage locations'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.storage.location.sequence',
            'view_mode': 'list',
            'domain': [('package_storage_type_id', '=', self.id)],
            'context': {'default_package_storage_type_id': self.id},
        }
