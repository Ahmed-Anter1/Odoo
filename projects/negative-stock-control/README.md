# Location-Level Negative Stock Control

## Overview

A reusable inventory control that blocks stock operations when they would create a negative quantity in an internal location.

## Implemented Capabilities

- Checks immediately before stock posting
- Location-specific availability validation
- Coverage for sales, transfers, returns, and adjustments
- Product and location details in validation messages
- Integration with accelerated sale workflows
- Protection against partial workflow side effects

## Technical Areas

Odoo 18, Inventory, stock moves, stock move lines, Python overrides, validation, and location-aware quantities.

## Engineering Focus

The check runs at the final stock-operation boundary and can also be called earlier by automated workflows, preventing business steps from continuing when stock is insufficient.
