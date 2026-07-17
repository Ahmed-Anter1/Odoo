"""Independent portfolio example: opt-in MRP batch scaling."""

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    enable_batch_scaling = fields.Boolean()
    batch_count = fields.Float(default=1.0)
    machine_size = fields.Float(default=1.0)

    @api.onchange("enable_batch_scaling", "batch_count", "machine_size")
    def _onchange_batch_scaling(self):
        for production in self:
            production._apply_batch_scaling()

    @api.model_create_multi
    def create(self, vals_list):
        productions = super().create(vals_list)
        productions.with_context(skip_batch_scaling=True)._apply_batch_scaling()
        return productions

    def write(self, vals):
        result = super().write(vals)
        trigger_fields = {"enable_batch_scaling", "batch_count", "machine_size"}
        if trigger_fields.intersection(vals) and not self.env.context.get(
            "skip_batch_scaling"
        ):
            self.with_context(skip_batch_scaling=True)._apply_batch_scaling()
        return result

    def _apply_batch_scaling(self):
        for production in self.filtered("enable_batch_scaling"):
            factor = max(production.batch_count, 0.0) * max(
                production.machine_size, 0.0
            )
            if float_compare(
                production.product_qty,
                factor,
                precision_rounding=production.product_uom_id.rounding,
            ) != 0:
                production.with_context(skip_batch_scaling=True).product_qty = factor

            for move in production.move_raw_ids.filtered(
                lambda item: item.state not in ("done", "cancel")
            ):
                base_quantity = move.bom_line_id.product_qty if move.bom_line_id else 0.0
                move.product_uom_qty = base_quantity * factor
