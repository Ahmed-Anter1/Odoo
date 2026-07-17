# Serial Return Wizard

## Overview

An Odoo assistant that locates a sold serial number and guides the user to its related delivery, sale, and invoice information before processing a return.

## Implemented Capabilities

- Search by serial or lot number
- Product and customer identification
- Related delivery and sale-order lookup
- Related invoice navigation
- Validation of serial history
- Clear return context before users take action

## Technical Areas

Odoo 18, Inventory, Sales, Accounting, stock lots, stock move lines, transient models, ORM searches, and XML views.

## Engineering Focus

The wizard starts from the physical serial number and reconstructs its commercial history, reducing incorrect returns and manual record searching.
