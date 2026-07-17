"""Independent portfolio example: record access by allowed journals and partners."""

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    restricted_accounting_access = fields.Boolean()
    allowed_journal_ids = fields.Many2many("account.journal")
    allowed_partner_ids = fields.Many2many("res.partner")


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        if user.restricted_accounting_access and not user._is_admin():
            domain = list(domain) + [("id", "in", user.allowed_journal_ids.ids)]
        return super()._search(domain, offset=offset, limit=limit, order=order)


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        user = self.env.user
        if user.restricted_accounting_access and not user._is_admin():
            domain = list(domain)
            domain += [("journal_id", "in", user.allowed_journal_ids.ids)]
            if user.allowed_partner_ids:
                domain += [("partner_id", "in", user.allowed_partner_ids.ids)]
        return super()._search(domain, offset=offset, limit=limit, order=order)

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        user = self.env.user
        if user.restricted_accounting_access and not user._is_admin():
            forbidden = moves.filtered(
                lambda move: move.journal_id not in user.allowed_journal_ids
            )
            forbidden.check_access("write")
        return moves
