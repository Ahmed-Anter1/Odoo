"""Independent portfolio example: cumulative transaction-currency balance."""

from collections import defaultdict

from odoo import models


class PartnerLedgerCurrencyBalance(models.AbstractModel):
    _inherit = "account.partner.ledger.report.handler"

    def _query_currency_balances(self, options, partner_ids=None):
        """Return signed amount_currency grouped by partner and currency."""
        report = self.env["account.report"].browse(options["report_id"])
        tables, where_clause, where_params = report._query_get(
            options,
            "strict_range",
            domain=[("partner_id", "in", partner_ids)] if partner_ids else None,
        )
        query = f"""
            SELECT
                account_move_line.partner_id,
                account_move_line.currency_id,
                COALESCE(SUM(account_move_line.amount_currency), 0.0) AS balance
            FROM {tables}
            WHERE {where_clause}
              AND account_move_line.currency_id IS NOT NULL
            GROUP BY
                account_move_line.partner_id,
                account_move_line.currency_id
        """
        self.env.cr.execute(query, where_params)
        balances = defaultdict(dict)
        for row in self.env.cr.dictfetchall():
            balances[row["partner_id"]][row["currency_id"]] = row["balance"]
        return balances

    def add_running_currency_balance(self, lines, opening_balances=None):
        """Add a display value while keeping calculation state per currency."""
        running = defaultdict(float)
        for currency_id, amount in (opening_balances or {}).items():
            running[currency_id] = amount

        for line in lines:
            currency_id = line.get("currency_id")
            if not currency_id:
                line["currency_balance"] = None
                continue
            running[currency_id] += line.get("amount_currency", 0.0)
            line["currency_balance"] = running[currency_id]
        return lines
