# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from copy import deepcopy

FIELDS_RELATED = [
    "product_tmpl_id",
    "name",
    "product_id",
    "product_name",
    "product_code",
    "sequence",
]

FIELDS_MATCH_GROUP = [
    "product_tmpl_id",
    "name",
    "product_id",
    "product_name",
    "product_code",
]


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    supplierinfo_group_id = fields.Many2one("product.supplierinfo.group", required=True)
    product_tmpl_id = fields.Many2one(related="supplierinfo_group_id.product_tmpl_id")
    name = fields.Many2one(related="supplierinfo_group_id.name")
    product_id = fields.Many2one(related="supplierinfo_group_id.product_id")
    product_name = fields.Char(related="supplierinfo_group_id.product_name")
    product_code = fields.Char(related="supplierinfo_group_id.product_code")
    sequence = fields.Integer(related="supplierinfo_group_id.sequence")

    def _find_or_create_supplierinfo_group(self, vals):
        domain = [(field, "=", vals.get(field)) for field in FIELDS_MATCH_GROUP]
        group = self.env["product.supplierinfo.group"].search(domain)
        if not group:
            group = self.env["product.supplierinfo.group"].create(
                {field: vals.get(field) for field in FIELDS_MATCH_GROUP}
            )
        return group

    def to_supplierinfo_group(self, vals):
        new_val = deepcopy(vals)
        group = self.env["product.supplierinfo.group"].browse(
            new_val.get("supplierinfo_group_id")
        ) or self._find_or_create_supplierinfo_group(new_val)
        new_val["supplierinfo_group_id"] = group.id
        for field in FIELDS_RELATED:
            if field in new_val:
                del new_val[field]
        return new_val

    @api.model_create_multi
    def create(self, vals):
        new_vals = []
        for el in vals:
            new_vals.append(self.to_supplierinfo_group(el))
        return super().create(new_vals)
