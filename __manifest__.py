{
    "name": "Fit It Sales Reports",
    "summary": "Custom quotation and service reports for Fit It on Odoo 19",
    "version": "19.0.1.0.0",
    "category": "Sales/Sales",
    "author": "Fit It",
    "license": "LGPL-3",
    "depends": ["sale_management"],
    "data": [
        "views/sale_order_views.xml",
        "report/paperformat.xml",
        "report/sale_order_reports.xml",
        "report/sale_order_templates.xml",
    ],
    "installable": True,
    "application": False,
}
