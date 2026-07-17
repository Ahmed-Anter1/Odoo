# Landed Cost & Purchase Currency Enhancements

## Overview

Odoo inventory and purchasing enhancements that make original purchase-currency values visible during landed-cost valuation.

## Implemented Capabilities

- Original purchase unit price on valuation adjustment lines
- Purchase currency visibility
- Product value in transaction currency
- Import-cost total calculation
- Purchase-line lookup through related stock moves
- UoM-aware unit-price conversion
- Company-currency and foreign-currency separation

## Technical Areas

Odoo 18, Inventory, Purchase, Landed Costs, stock valuation, multi-currency, computed fields, and ORM relationships.

## Engineering Focus

The calculations trace valuation lines back to their originating purchase data and keep operational foreign-currency values separate from accounting valuation amounts.
