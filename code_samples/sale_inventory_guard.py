"""Independent portfolio example: guarded one-click sale processing."""

from collections import defaultdict

from odoo import _, models
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _required_stock_by_product(self):
        self.ensure_one()
        required = defaultdict(float)
        for line in self.order_line.filtered(
            lambda item: not item.display_type and item.product_id.type == "consu"
        ):
            quantity = line.product_uom._compute_quantity(
                line.product_uom_qty,
                line.product_id.uom_id,
            )
            required[line.product_id] += quantity
        return required

    def _check_available_stock(self):
        """Validate quantities before confirmation without changing stock."""
        self.ensure_one()
        warehouse = self.warehouse_id
        if not warehouse:
            raise UserError(_("Select a warehouse before processing the sale."))

        shortages = []
        for product, required in self._required_stock_by_product().items():
            available = product.with_context(
                location=warehouse.lot_stock_id.id
            ).free_qty
            if available < required:
                shortages.append(
                    _("%(product)s: required %(required)s, available %(available)s")
                    % {
                        "product": product.display_name,
                        "required": required,
                        "available": available,
                    }
                )

        if shortages:
            raise ValidationError(
                _("The sale would create insufficient stock:\n%s")
                % "\n".join(shortages)
            )

    def action_complete_sale_safely(self):
        """Confirm, reserve, validate delivery, then prepare an invoice."""
        for order in self:
            if order.state not in ("draft", "sent"):
                raise UserError(_("Only quotations can use the complete-sale action."))

            order._check_available_stock()
            order.action_confirm()

            for picking in order.picking_ids.filtered(
                lambda record: record.state not in ("done", "cancel")
            ):
                picking.action_assign()
                if any(
                    move.product_uom_qty > move.quantity
                    for move in picking.move_ids.filtered(
                        lambda move: move.state not in ("done", "cancel")
                    )
                ):
                    raise UserError(
                        _("Delivery %(picking)s is not fully reserved.")
                        % {"picking": picking.name}
                    )
                picking.button_validate()

            invoice = order._create_invoices()
            return {
                "type": "ir.actions.act_window",
                "name": _("Customer Invoice"),
                "res_model": "account.move",
                "view_mode": "form",
                "res_id": invoice.id,
            }


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_done(self, cancel_backorder=False):
        """Run a location-level guard immediately before final stock posting."""
        for move in self.filtered(
            lambda record: record.product_id.type == "consu"
            and record.location_id.usage == "internal"
        ):
            available = move.product_id.with_context(
                location=move.location_id.id
            ).qty_available
            outgoing = sum(
                move.move_line_ids.filtered(
                    lambda line: line.location_id == move.location_id
                ).mapped("quantity")
            )
            if outgoing > available:
                raise ValidationError(
                    _("Insufficient stock for %(product)s in %(location)s.")
                    % {
                        "product": move.product_id.display_name,
                        "location": move.location_id.display_name,
                    }
                )
        return super()._action_done(cancel_backorder=cancel_backorder)
