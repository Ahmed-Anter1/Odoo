# Role-Based Access Control

## Overview

A centralized Odoo security layer for managing user access to menus, models, fields, buttons, filters, accounting records, and business partners.

## Implemented Capabilities

- Reusable access roles assigned to users
- Menu and model access restrictions
- Field-level read and write controls
- Button, tab, filter, and group-by visibility rules
- Record-rule integration
- User-specific journal, account, and partner access
- Safe synchronization between roles and user groups

## Technical Areas

Odoo 18, Python, security groups, access-control lists, record rules, view architecture, ORM hooks, menus, and XML.

## Engineering Focus

The design groups permissions into maintainable roles instead of relying on scattered user-by-user configuration, while preserving standard Odoo security behavior.
