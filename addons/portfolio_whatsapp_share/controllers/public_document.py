import secrets

from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound


class PortfolioPublicDocument(http.Controller):

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
        return request.make_response(
            pdf,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Disposition", f'inline; filename="{order.name}.pdf"'),
                ("Cache-Control", "no-store"),
            ],
        )
