# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND
from odoo.tools import float_compare
from odoo.tools.safe_eval import const_eval


class DeliveryCarrierPreference(models.Model):

    _name = "delivery.carrier.preference"
    _description = "Preferred Shipping Methods"
    _order = "sequence, id"

    sequence = fields.Integer(required=True, default=10, index=True)
    name = fields.Char(compute="_compute_name", readonly=True)
    preference = fields.Selection(
        [("carrier", "Defined carrier"), ("partner", "Partner carrier")],
        required=True,
        default="carrier",
    )
    carrier_id = fields.Many2one("delivery.carrier", ondelete="cascade")
    max_weight = fields.Float("Max weight", help="Leave empty for no limit")
    max_weight_uom_id = fields.Many2one(
        compute="_compute_max_weight_uom_id", readonly=True
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    picking_domain = fields.Char(
        default=[],
        help="Domain to restrict application of this preference "
        "for carrier selection on pickings",
    )

    @api.constrains("preference", "carrier_id")
    def _check_preference_carrier_id(self):
        for pref in self:
            if pref.preference == "carrier" and not pref.carrier_id:
                raise ValidationError(
                    _(
                        "Preferred Shipping Methods with 'Carrier' preference "
                        "must define a Delivery carrier."
                    )
                )
        partner_pref_cnt = self.search_count(
            [("preference", "=", "partner"), ("company_id", "=", self.env.company.id)]
        )
        if partner_pref_cnt > 1:
            raise ValidationError(
                _(
                    "Only one Preferred Shipping Method can be set with "
                    "'Partner carrier' preference."
                )
            )

    @api.constrains("max_weight")
    def _check_max_weight(self):
        for pref in self:
            if (
                float_compare(
                    pref.max_weight,
                    0,
                    precision_rounding=pref.max_weight_uom_id.rounding,
                )
                < 0
            ):
                raise ValidationError(
                    _("Max weight must have a positive or null value.")
                )

    @api.onchange("preference")
    def onchange_preference(self):
        self.ensure_one()
        if self.preference == "partner" and self.carrier_id:
            self.carrier_id = False

    @api.depends("preference", "carrier_id", "max_weight")
    def _compute_name(self):
        pref_descr = {
            k: v for k, v in self._fields["preference"]._description_selection(self.env)
        }
        for pref in self:
            name = pref_descr.get(pref.preference)
            if pref.carrier_id:
                name = _("%s: %s") % (name, pref.carrier_id.name)
            if pref.max_weight:
                name = _("%s (Max weight %s %s)") % (
                    name,
                    pref.max_weight,
                    pref.max_weight_uom_id.display_name,
                )
            pref.name = name

    def _compute_max_weight_uom_id(self):
        for pref in self:
            pref.max_weight_uom_id = (
                self.env["product.template"]
                ._get_weight_uom_id_from_ir_config_parameter()
                .id
            )

    @api.model
    def get_preferred_carriers(self, partner, weight, company, picking=None):
        # TODO Check possible conflicting settings between doc company and
        #  user preference defined on another company?
        company_carriers = self.env["delivery.carrier"].search(
            ["|", ("company_id", "=", False), ("company_id", "=", company.id)]
        )
        carrier_preferences = self.search(
            [
                "&",
                "|",
                ("max_weight", ">=", weight),
                ("max_weight", "=", 0.0),
                "|",
                ("carrier_id", "in", company_carriers.ids),
                ("carrier_id", "=", False),
            ]
        )
        carriers_ids = list()
        for cp in carrier_preferences:
            if (
                picking is not None
                and cp.picking_domain
                and not cp._is_valid_for_picking(picking)
            ):
                continue
            if cp.preference == "carrier":
                carriers_ids.append(cp.carrier_id.id)
            else:
                partner_carrier = partner.property_delivery_carrier_id
                if partner_carrier:
                    carriers_ids.append(partner_carrier.id)
        return (
            self.env["delivery.carrier"]
            .browse(carriers_ids)
            .available_carriers(partner)
        )

    def _is_valid_for_picking(self, picking):
        self.ensure_one()
        domain = const_eval(self.picking_domain)
        if not domain:
            return True
        else:
            return self.env["stock.picking"].search_count(
                AND(domain, [("id", "=", picking.id)])
            )
