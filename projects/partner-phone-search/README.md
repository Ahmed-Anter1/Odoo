# Partner Search by Phone Number

## Overview

An Odoo contact-search enhancement that helps users find customers and vendors using phone or mobile numbers from business documents.

## Implemented Capabilities

- Phone and mobile matching in partner display-name searches
- Support from Sales and Purchase partner selectors
- Partial-number search
- Compatibility with standard name and reference searches
- Normalized behavior across contact lookups

## Technical Areas

Odoo 18, Contacts, ORM search methods, domain composition, Sales, Purchase, and Python.

## Engineering Focus

The extension adds phone criteria without replacing Odoo's standard search behavior, allowing users to find records using the information available during calls and messages.
