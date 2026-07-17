# Sales, Inventory & Accounting Automation

## Overview

A group of connected Odoo customizations designed to shorten sales processing while preserving inventory and accounting controls.

## Implemented Capabilities

- Customer-authorized pricelists
- Best-price selection across eligible pricelists
- Currency conversion and exchange-rate visibility
- Last customer sale-price visibility
- Automated invoice creation and posting
- Payment workflow integration
- Serial-controlled quotations and deliveries
- Serial availability and duplication validation
- One-click sale confirmation, delivery, and invoicing
- Guided return workflow with automatic credit notes
- Location-level negative-stock prevention

## Technical Areas

Odoo 18, Python, ORM, Sales, Inventory, Accounting, multi-currency, pricelists, serial/lot tracking, stock moves, invoices, payments, and validation constraints.

## Engineering Decisions

Automation was placed behind explicit business actions and validation checks. Serial numbers, stock availability, invoice state, and return quantities are validated before irreversible workflow steps continue.

> This case study summarizes implementation experience without publishing client-specific rules, configurations, or proprietary code.
