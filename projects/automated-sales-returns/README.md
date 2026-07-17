# Automated Sales Returns & Credit Notes

## Overview

A guided Odoo return workflow that connects Sales, Inventory, and Accounting to reduce the manual steps required to process product and service returns.

## Implemented Capabilities

- Return action directly from the sale order
- Selection of returnable products and quantities
- Serial-number selection for tracked products
- Automatic stock return creation and confirmation
- Service-return handling without stock moves
- Automatic customer credit-note creation
- Financial line validation before invoice reversal
- Separate return-only and return-with-credit-note actions

## Technical Areas

Odoo 18, Sales, Inventory, Accounting, stock return wizards, serial/lot tracking, credit notes, Python, and XML views.

## Engineering Focus

The workflow keeps inventory and financial returns synchronized while validating quantities, serial numbers, source documents, and invoice state before posting changes.
