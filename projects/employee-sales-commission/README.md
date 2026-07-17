# Employee Sales Commission

## Overview

An Odoo workflow for distributing sales commissions across multiple employees and recording the resulting accounting entries.

## Implemented Capabilities

- Multiple employees per sale order
- Percentage-based and fixed-amount commission options
- Automatic commission calculation
- Validation of distribution values
- Journal-entry creation after confirmation
- Expense and payable account integration
- Refund-aware commission adjustment
- Traceability between sale orders and accounting moves

## Technical Areas

Odoo 18, Sales, Employees, Accounting, Python, computed and inverse fields, journal entries, and XML views.

## Engineering Focus

Commission calculation and posting are separated so users can review the distribution before accounting entries are created.
