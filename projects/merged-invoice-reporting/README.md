# Merged Invoice Reporting

## Overview

A custom accounting report that combines multiple invoices for the same customer into one readable sales and returns summary.

## Implemented Capabilities

- Multi-invoice selection and validation
- Grouping by customer and product
- Sold and returned quantities shown separately
- Net quantity and total calculations
- Average-price calculation
- Tax-aware totals
- Arabic-ready QWeb/PDF output
- Navigation back to related sales documents

## Technical Areas

Odoo 18, Accounting, Python, transient models, QWeb/PDF, report actions, aggregation, and XML.

## Engineering Focus

The report normalizes invoice and refund lines into a consistent dataset before rendering, making the output easier to audit and reuse.
