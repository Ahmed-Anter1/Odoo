# Customer Statements & Multi-Currency Reporting

## Overview

Custom Odoo accounting workflows and reports that provide clearer customer activity and foreign-currency balances.

## Implemented Capabilities

- Customer statement generation by partner and date range
- Invoice, return, and payment breakdowns
- Cash-in and cash-out tracking
- Opening and closing balance calculation
- Product-category filtering
- On-screen preview before report generation
- QWeb/PDF output
- Excel export with structured sheets
- Cumulative foreign-currency balance in General Ledger
- Initial, running, and ending currency balances in Partner Ledger

## Technical Areas

Odoo 18, Accounting, account reports, Python, ORM, SQL-aware reporting, QWeb/PDF, Excel generation, multi-currency, and reconciliation support.

## Engineering Decisions

The reporting flow builds a consistent data structure that can be reused by preview, PDF, and Excel outputs. Currency calculations are kept separate from company-currency totals to make reconciliation easier to understand.

> No financial records, customer identities, report samples, or proprietary source code are included.
