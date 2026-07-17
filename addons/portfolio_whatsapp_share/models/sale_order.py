import secrets
import urllib.parse

from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    portfolio_share_token = fields.Char(copy=False, groups="base.group_system")

    def _ensure_share_token(self):
        for order in self:
            if not order.portfolio_share_token:
                order.sudo().portfolio_share_token = secrets.token_urlsafe(24)

    def action_share_quotation_whatsapp(self):
        self.ensure_one()
        self._ensure_share_token()
        raw_phone = self.partner_id.mobile or self.partner_id.phone or ""
        phone = "".join(char for char in raw_phone if char.isdigit())
        if not phone:
            raise UserError(_("Add a phone or mobile number to the customer."))

        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        pdf_url = f"{base_url}/portfolio/quotation/{self.id}/{self.portfolio_share_token}"
        message = _("Hello %(name)s, quotation %(order)s: %(url)s") % {
            "name": self.partner_id.name,
            "order": self.name,
            "url": pdf_url,
        }
        return {
            "type": "ir.actions.act_url",
            "url": f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}",
            "target": "new",
        }
