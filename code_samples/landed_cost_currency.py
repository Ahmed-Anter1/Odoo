"""Independent portfolio example: purchase-currency values on landed costs."""

from odoo import api, fields, models


class StockValuationAdjustmentLines(models.Model):
    _inherit = "stock.valuation.adjustment.lines"

    purchase_currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_purchase_currency_values",
    )
    purchase_unit_price = fields.Monetary(
        currency_field="purchase_currency_id",
        compute="_compute_purchase_currency_values",
    )
    purchase_subtotal = fields.Monetary(
        currency_field="purchase_currency_id",
        compute="_compute_purchase_currency_values",
    )

    @api.depends("move_id", "product_id", "quantity")
    def _compute_purchase_currency_values(self):
        for line in self:
            line.purchase_currency_id = False
            line.purchase_unit_price = 0.0
            line.purchase_subtotal = 0.0

            purchase_line = line.move_id.purchase_line_id
            if not purchase_line or purchase_line.product_id != line.product_id:
                continue

            line.purchase_currency_id = purchase_line.currency_id
            unit_price = purchase_line.product_uom._compute_price(
                purchase_line.price_unit,
                line.product_id.uom_id,
            )
            line.purchase_unit_price = unit_price
            line.purchase_subtotal = unit_price * line.quantity


class StockLandedCost(models.Model):
    _inherit = "stock.landed.cost"

    import_cost_total_company_currency = fields.Monetary(
        compute="_compute_import_cost_total",
        currency_field="company_currency_id",
    )
    company_currency_id = fields.Many2one(
        related="company_id.currency_id",
        readonly=True,
    )

    @api.depends("valuation_adjustment_lines.additional_landed_cost")
    def _compute_import_cost_total(self):
        for cost in self:
            cost.import_cost_total_company_currency = sum(
                cost.valuation_adjustment_lines.mapped("additional_landed_cost")
            )
