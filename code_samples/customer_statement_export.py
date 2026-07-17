"""Independent portfolio example: reusable customer-statement dataset and export action."""

import base64
import io
from datetime import date

import xlsxwriter

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CustomerStatementWizard(models.TransientModel):
    _name = "portfolio.customer.statement.wizard"
    _description = "Portfolio Customer Statement"

    partner_id = fields.Many2one("res.partner", required=True)
    date_from = fields.Date(required=True, default=lambda self: date.today().replace(day=1))
    date_to = fields.Date(required=True, default=fields.Date.context_today)
    file_data = fields.Binary(readonly=True)
    file_name = fields.Char(readonly=True)

    def _statement_lines(self):
        self.ensure_one()
        domain = [
            ("partner_id", "=", self.partner_id.id),
            ("parent_state", "=", "posted"),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to),
            ("account_id.account_type", "in", ("asset_receivable", "liability_payable")),
        ]
        move_lines = self.env["account.move.line"].search(domain, order="date, id")
        running_balance = 0.0
        result = []
        for line in move_lines:
            running_balance += line.debit - line.credit
            result.append(
                {
                    "date": line.date,
                    "reference": line.move_name,
                    "label": line.name,
                    "debit": line.debit,
                    "credit": line.credit,
                    "balance": running_balance,
                }
            )
        return result

    def action_export_xlsx(self):
        self.ensure_one()
        if self.date_from > self.date_to:
            raise ValidationError(_("The start date must not be after the end date."))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet("Statement")
        header = workbook.add_format({"bold": True, "bg_color": "#D9EAF7"})
        money = workbook.add_format({"num_format": "#,##0.00"})

        columns = ["Date", "Reference", "Description", "Debit", "Credit", "Balance"]
        for column, title in enumerate(columns):
            sheet.write(0, column, title, header)

        for row, item in enumerate(self._statement_lines(), start=1):
            sheet.write(row, 0, str(item["date"]))
            sheet.write(row, 1, item["reference"])
            sheet.write(row, 2, item["label"])
            sheet.write_number(row, 3, item["debit"], money)
            sheet.write_number(row, 4, item["credit"], money)
            sheet.write_number(row, 5, item["balance"], money)

        sheet.set_column(0, 0, 12)
        sheet.set_column(1, 2, 25)
        sheet.set_column(3, 5, 14)
        workbook.close()

        self.write(
            {
                "file_data": base64.b64encode(output.getvalue()),
                "file_name": f"statement-{self.partner_id.id}.xlsx",
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": (
                f"/web/content/{self._name}/{self.id}/file_data/"
                f"{self.file_name}?download=true"
            ),
            "target": "self",
        }
