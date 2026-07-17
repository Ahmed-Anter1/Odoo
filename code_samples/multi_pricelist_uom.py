"""Independent portfolio example: customer-authorized pricelists and UoM prices."""

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    allowed_pricelist_ids = fields.Many2many(
        "product.pricelist",
        string="Allowed Pricelists",
    )


class ProductUomPrice(models.Model):
    _name = "portfolio.product.uom.price"
    _description = "Portfolio Product UoM Price"

    product_tmpl_id = fields.Many2one("product.template", required=True, ondelete="cascade")
    uom_id = fields.Many2one("uom.uom", required=True)
    price = fields.Monetary(required=True)
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    _sql_constraints = [
        (
            "unique_product_uom_currency",
            "unique(product_tmpl_id, uom_id, currency_id)",
            "Only one price is allowed per product, unit, and currency.",
        )
    ]


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    selected_pricelist_id = fields.Many2one("product.pricelist", copy=False)

    @api.onchange("product_id", "product_uom", "order_id.partner_id")
    def _onchange_find_best_allowed_price(self):
        for line in self.filtered(lambda item: item.product_id and item.order_id.partner_id):
            partner = line.order_id.partner_id
            allowed = partner.allowed_pricelist_ids
            if not allowed:
                continue

            candidates = []
            for pricelist in allowed:
                price = pricelist._get_product_price(
                    line.product_id,
                    line.product_uom_qty or 1.0,
                    currency=line.order_id.currency_id,
                    uom=line.product_uom,
                    date=line.order_id.date_order,
                )
                candidates.append((price, pricelist))

            positive = [item for item in candidates if item[0] > 0]
            if positive:
                line.price_unit, line.selected_pricelist_id = min(
                    positive, key=lambda item: item[0]
                )

    @api.constrains("selected_pricelist_id", "order_id.partner_id")
    def _check_pricelist_is_allowed(self):
        for line in self.filtered("selected_pricelist_id"):
            if line.selected_pricelist_id not in line.order_id.partner_id.allowed_pricelist_ids:
                raise ValidationError(_("The selected pricelist is not allowed for this customer."))
