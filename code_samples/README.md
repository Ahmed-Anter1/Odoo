# Odoo Code Samples

These independently written samples demonstrate reusable Odoo engineering patterns from my experience.

They are intentionally generic and do not contain client names, credentials, endpoints, database records, production configurations, or proprietary business logic.

## Integrations & Communication

- [Generic B2B Connector](generic_b2b_connector.py): configuration, validation, payload preparation, API calls, and structured logs.
- [Secure WhatsApp Documents](secure_whatsapp_documents.py): token-protected PDF routes and message preparation.

## Sales & Inventory

- [Sales & Inventory Guard](sale_inventory_guard.py): controlled sale processing and stock validation.
- [Serial Quotation Workflow](serial_quotation_workflow.py): serial selection, validation, and transfer to delivery operations.
- [Multi-Pricelist & UoM Pricing](multi_pricelist_uom.py): customer-authorized pricelists, best-price selection, and unit pricing.

## Accounting & Reporting

- [Customer Statement Export](customer_statement_export.py): reusable statement dataset and Excel output.
- [Currency Balance Report Extension](currency_balance_report.py): cumulative foreign-currency balances.
- [Landed Cost Currency Values](landed_cost_currency.py): purchase-currency values and import-cost totals.

## Manufacturing & Security

- [MRP Batch Scaling](mrp_batch_scaling.py): controlled production and component quantity scaling.
- [Accounting Access Control](access_control_rules.py): user-specific journal and partner access patterns.

These files are portfolio examples rather than installable production modules. Full Odoo modules normally also include manifests, access controls, XML views, tests, and translations.
