# Sensitive Data & Menu Security

## Overview

A set of Odoo access improvements that limits sensitive cost information and hides selected menus for specific users.

## Implemented Capabilities

- Restriction of product cost-price visibility
- Security-group-based field access
- User-specific hidden menus
- Admin-safe behavior
- Dynamic menu filtering
- Preservation of standard menu access for unrestricted users
- Centralized user configuration

## Technical Areas

Odoo 18, Product, Inventory, menus, security groups, user preferences, ORM overrides, and XML security definitions.

## Engineering Focus

The controls protect sensitive information at both the interface and access-rule levels while avoiding changes for administrators and authorized users.
