# Manufacturing Batch Scaling & WhatsApp Documents

## Overview

Two Odoo 19 customizations supporting manufacturing quantity planning and faster document communication.

## Manufacturing Batch Scaling

- Configurable batch multiplier on manufacturing orders
- Optional machine-size factor
- Automatic recalculation of production and component quantities
- Controlled update behavior across onchange, create, and write operations
- Context protection to avoid recursive recalculation

## WhatsApp Document Sharing

- WhatsApp actions on quotations, invoices, and delivery records
- Phone-number and message preparation from Odoo business records
- Secure random tokens for public document links
- Token-protected quotation and invoice PDF routes
- URL encoding for message content

## Technical Areas

Odoo 19, Python, MRP, Sales, Inventory, Accounting, computed fields, onchange logic, HTTP controllers, secure tokens, QWeb/PDF, and WhatsApp Web links.

## Engineering Decisions

Manufacturing calculations are opt-in and protected against repeated write cycles. Public document routes validate record-specific tokens before rendering a PDF.

> This case study contains no customer contact information, documents, tokens, production formulas, or proprietary source code.
