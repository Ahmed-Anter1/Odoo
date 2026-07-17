# Inventory Pricelist Visibility

## Overview

An inventory enhancement that displays selected sales pricelists alongside product stock information.

## Implemented Capabilities

- Pricelist values visible from inventory quantities
- User-specific pricelist selection
- Product price calculation across multiple pricelists
- Currency-aware price display
- Export-friendly pricing values
- Persistent user preferences
- Product-level price lookup actions

## Technical Areas

Odoo 18, Inventory, Product, Sales Pricelists, multi-currency, computed fields, JSON data, user preferences, and export customization.

## Engineering Focus

Pricing data is computed only for the pricelists selected by each user, keeping inventory screens useful without loading every available price rule.
