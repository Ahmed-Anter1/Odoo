"""Independent portfolio example: serial-number selection on quotation lines."""

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    quotation_lot_ids = fields.Many2many(
        "stock.lot",
        string="Reserved Serials",
        domain="[('product_id', '=', product_id)]",
        copy=False,
    )
    requires_serial = fields.Boolean(compute="_compute_requires_serial")

    @api.depends("product_id.tracking")
    def _compute_requires_serial(self):
        for line in self:
            line.requires_serial = line.product_id.tracking == "serial"

    @api.constrains("quotation_lot_ids", "product_uom_qty")
    def _check_serial_quantity(self):
        for line in self.filtered("requires_serial"):
            if len(line.quotation_lot_ids) != int(line.product_uom_qty):
                raise ValidationError(
                    _("Select exactly one serial number for each ordered unit.")
                )

    @api.constrains("quotation_lot_ids")
    def _check_duplicate_serials(self):
        for line in self:
            duplicates = line.order_id.order_line.filtered(
                lambda other: other != line
                and bool(other.quotation_lot_ids & line.quotation_lot_ids)
            )
            if duplicates:
                raise ValidationError(_("A serial number cannot be used twice in one order."))


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            order.order_line.filtered("requires_serial")._check_serial_quantity()
        result = super().action_confirm()
        self._assign_quotation_serials_to_pickings()
        return result

    def _assign_quotation_serials_to_pickings(self):
        for order in self:
            for picking in order.picking_ids.filtered(
                lambda record: record.state not in ("done", "cancel")
            ):
                for move in picking.move_ids:
                    sale_line = move.sale_line_id
                    if not sale_line.quotation_lot_ids:
                        continue
                    move.move_line_ids.unlink()
                    for lot in sale_line.quotation_lot_ids:
                        self.env["stock.move.line"].create(
                            {
                                "move_id": move.id,
                                "picking_id": picking.id,
                                "product_id": move.product_id.id,
                                "product_uom_id": move.product_uom.id,
                                "quantity": 1.0,
                                "lot_id": lot.id,
                                "location_id": move.location_id.id,
                                "location_dest_id": move.location_dest_id.id,
                            }
                        )
