# Odoo Code Samples

These independently written samples demonstrate reusable Odoo engineering patterns from my experience.

They are intentionally generic and do not contain client names, credentials, endpoints, database records, production configurations, or proprietary business logic.

## Samples

- [Generic B2B Connector](generic_b2b_connector.py): configuration, validation, payload preparation, API calls, and structured logs.
- [Sales & Inventory Guard](sale_inventory_guard.py): controlled sale processing and stock validation.
- [Currency Balance Report Extension](currency_balance_report.py): cumulative foreign-currency balances.
- [MRP Batch Scaling](mrp_batch_scaling.py): controlled production and component quantity scaling.

These files are portfolio examples rather than installable production modules. Full Odoo modules normally also include manifests, access controls, XML views, tests, and translations.
