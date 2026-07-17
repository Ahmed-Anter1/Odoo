"""Independent portfolio example: a generic external B2B connector for Odoo 18."""

import json
import logging

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PortfolioApiLog(models.Model):
    _name = "portfolio.api.log"
    _description = "Portfolio API Log"
    _order = "create_date desc"

    name = fields.Char(required=True)
    direction = fields.Selection(
        [("out", "Odoo to External"), ("in", "External to Odoo")],
        required=True,
        default="out",
    )
    endpoint = fields.Char(required=True)
    request_payload = fields.Text()
    response_payload = fields.Text()
    http_status = fields.Integer()
    success = fields.Boolean(default=False)
    error_message = fields.Text()


class PortfolioApiConfig(models.Model):
    _name = "portfolio.api.config"
    _description = "Portfolio API Configuration"

    name = fields.Char(required=True, default="External B2B")
    base_url = fields.Char(required=True)
    access_token = fields.Char(groups="base.group_system")
    timeout_seconds = fields.Integer(default=20)
    active = fields.Boolean(default=True)

    @api.constrains("base_url")
    def _check_base_url(self):
        for config in self:
            if not config.base_url.startswith(("https://", "http://")):
                raise ValidationError(_("The API URL must start with http:// or https://"))

    def _headers(self):
        self.ensure_one()
        if not self.access_token:
            raise UserError(_("Configure an access token before sending data."))
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _endpoint_url(self, endpoint):
        self.ensure_one()
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def call_api(self, method, endpoint, payload=None):
        """Send a JSON request and always create a support-friendly log."""
        self.ensure_one()
        url = self._endpoint_url(endpoint)
        log = self.env["portfolio.api.log"].sudo().create(
            {
                "name": f"{method.upper()} {endpoint}",
                "endpoint": endpoint,
                "request_payload": json.dumps(payload or {}, indent=2, default=str),
            }
        )

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=self._headers(),
                json=payload,
                timeout=max(self.timeout_seconds, 1),
            )
            safe_response = response.text[:10000]
            log.write(
                {
                    "http_status": response.status_code,
                    "response_payload": safe_response,
                    "success": response.ok,
                }
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except (requests.RequestException, ValueError) as exc:
            log.write({"success": False, "error_message": str(exc)})
            _logger.exception("External B2B request failed: %s", endpoint)
            raise UserError(_("The external service request failed. Review API Logs.")) from exc


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    external_export_state = fields.Selection(
        [("draft", "Not Prepared"), ("ready", "Ready"), ("sent", "Sent")],
        default="draft",
        copy=False,
    )

    def _prepare_external_payload(self):
        self.ensure_one()
        if self.state not in ("purchase", "done"):
            raise UserError(_("Confirm the purchase order before preparing an export."))
        if not self.partner_id.email:
            raise UserError(_("The vendor must have an email address."))

        lines = []
        for line in self.order_line.filtered(lambda item: not item.display_type):
            if line.product_qty <= 0:
                raise ValidationError(_("Export quantities must be positive."))
            lines.append(
                {
                    "sku": line.product_id.default_code or str(line.product_id.id),
                    "quantity": line.product_qty,
                    "unit_price": line.price_unit,
                }
            )
        return {
            "reference": self.name,
            "vendor": self.partner_id.name,
            "currency": self.currency_id.name,
            "lines": lines,
        }

    def action_mark_ready_for_external_export(self):
        for order in self:
            order._prepare_external_payload()
            order.external_export_state = "ready"

    def action_export_to_external_platform(self):
        config = self.env["portfolio.api.config"].search([("active", "=", True)], limit=1)
        if not config:
            raise UserError(_("Create an active API configuration first."))

        for order in self:
            if order.external_export_state != "ready":
                raise UserError(_("Approve the order for export first."))
            config.call_api("post", "/orders", order._prepare_external_payload())
            order.external_export_state = "sent"
