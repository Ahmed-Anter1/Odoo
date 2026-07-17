# Multi-Pricelist & UoM Pricing

## Overview

A flexible Odoo pricing workflow for customers who can purchase from multiple authorized pricelists and use product-specific unit-of-measure prices.

## Implemented Capabilities

- Customer-authorized pricelists
- Automatic best-price selection
- Currency conversion into the sale-order currency
- Exchange-rate visibility
- Last customer sale-price visibility
- Product and pricelist-specific UoM prices
- Secondary unit-of-measure support
- Manual-price protection and validation

## Technical Areas

Odoo 18, Sales, Product, Pricelists, UoM, multi-currency, Python, computed fields, onchange logic, constraints, and XML views.

## Engineering Focus

Pricing calculations respect the customer, selected unit, order currency, effective date, and explicit manual changes while preventing unauthorized pricelist use.
