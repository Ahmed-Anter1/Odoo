"""Independent portfolio example: token-protected document links for WhatsApp."""

import secrets
import urllib.parse

from odoo import fields, http, models
from odoo.http import request
from werkzeug.exceptions import NotFound


class SaleOrder(models.Model):
    _inherit = "sale.order"

    portfolio_share_token = fields.Char(copy=False, groups="base.group_system")

    def _ensure_portfolio_share_token(self):
        for order in self:
            if not order.portfolio_share_token:
                order.sudo().portfolio_share_token = secrets.token_urlsafe(24)

    def action_share_quotation_whatsapp(self):
        self.ensure_one()
        self._ensure_portfolio_share_token()
        phone = "".join(character for character in (self.partner_id.mobile or "") if character.isdigit())
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        pdf_url = (
            f"{base_url}/portfolio/quotation/{self.id}/"
            f"{self.portfolio_share_token}"
        )
        message = f"Hello {self.partner_id.name}, your quotation {self.name}: {pdf_url}"
        return {
            "type": "ir.actions.act_url",
            "url": f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}",
            "target": "new",
        }


class PortfolioDocumentController(http.Controller):

    @http.route(
        "/portfolio/quotation/<int:order_id>/<string:token>",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def quotation_pdf(self, order_id, token):
        order = request.env["sale.order"].sudo().browse(order_id).exists()
        if not order or not secrets.compare_digest(order.portfolio_share_token or "", token):
            raise NotFound()

        pdf, _ = request.env["ir.actions.report"].sudo()._render_qweb_pdf(
            "sale.action_report_saleorder",
            [order.id],
        )
        headers = [
            ("Content-Type", "application/pdf"),
            ("Content-Disposition", f'inline; filename="{order.name}.pdf"'),
            ("Cache-Control", "no-store"),
        ]
        return request.make_response(pdf, headers=headers)
