# Serial Numbers on Quotations

## Overview

An Odoo sales and inventory workflow that lets users select or import serial numbers directly on quotation lines and carries them into delivery operations.

## Implemented Capabilities

- Serial selection and text import from quotation lines
- Quantity-to-serial validation
- Duplicate-serial prevention within the same order
- Product and source-location validation
- Availability checks before confirmation
- Transfer of selected serials to stock move lines
- Clear serial status and count visibility

## Technical Areas

Odoo 18, Python, ORM, Sales, Inventory, stock lots, stock moves, wizards, constraints, and XML views.

## Engineering Focus

The workflow validates serial ownership, availability, duplicates, and required quantity before confirmation so incorrect tracking data cannot reach delivery operations.
