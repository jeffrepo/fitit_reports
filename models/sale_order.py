from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    fitit_report_template = fields.Selection(
        selection=[
            ("maintenance_report", "Reporte de mantenimiento"),
            ("bike_cash_finance", "Bicicletas: contado + financiamiento"),
            ("bike_rent_purchase", "Bicicletas: renta compra"),
            ("bike_msi", "Compra MSI"),
            ("gym_finance", "Financiamiento equipo gym"),
        ],
        string="Formato Fit It",
        default="bike_cash_finance",
        help=(
            "Formatos activos del machote 2026. Se omiten nota de remisión, "
            "cotización contado, cotización mantenimiento y cotización evento."
        ),
    )
    fitit_project_developer = fields.Char(string="Proyecto/desarrollador")
    fitit_contact_name = fields.Char(string="Contacto del cliente")
    fitit_contact_phone = fields.Char(string="Teléfono de contacto")
    fitit_customer_number = fields.Char(string="# Cliente")
    fitit_payment_method = fields.Char(string="Forma de pago", default="Pago de contado")
    fitit_quote_duration = fields.Char(string="Duración de cotización")
    fitit_contract_type = fields.Char(string="Tipo de contrato")
    fitit_service_date = fields.Date(string="Fecha de servicio")
    fitit_customer_observations = fields.Text(string="Observaciones del cliente")
    fitit_internal_notes = fields.Text(string="Notas para el reporte")
    fitit_down_payment = fields.Monetary(string="Anticipo", currency_field="currency_id")
    fitit_residual_payment = fields.Monetary(
        string="Pago final / valor residual", currency_field="currency_id"
    )
    fitit_financing_months = fields.Integer(string="Meses de financiamiento", default=12)
    fitit_interest_rate = fields.Float(string="Interés anual (%)")
    fitit_rental_months = fields.Integer(string="Meses de renta", default=12)
    fitit_msi_months = fields.Integer(string="Meses sin intereses", default=12)
    fitit_installation_fee = fields.Monetary(
        string="Instalación / envío", currency_field="currency_id"
    )
    fitit_financed_base = fields.Monetary(
        string="Base financiada", currency_field="currency_id", compute="_compute_fitit_amounts"
    )
    fitit_finance_total = fields.Monetary(
        string="Total financiado", currency_field="currency_id", compute="_compute_fitit_amounts"
    )
    fitit_finance_monthly_payment = fields.Monetary(
        string="Mensualidad financiamiento",
        currency_field="currency_id",
        compute="_compute_fitit_amounts",
    )
    fitit_rental_monthly_payment = fields.Monetary(
        string="Renta mensual", currency_field="currency_id", compute="_compute_fitit_amounts"
    )
    fitit_msi_monthly_payment = fields.Monetary(
        string="Pago mensual MSI", currency_field="currency_id", compute="_compute_fitit_amounts"
    )

    @api.depends(
        "amount_total",
        "fitit_down_payment",
        "fitit_residual_payment",
        "fitit_financing_months",
        "fitit_interest_rate",
        "fitit_rental_months",
        "fitit_msi_months",
        "fitit_installation_fee",
    )
    def _compute_fitit_amounts(self):
        for order in self:
            base = max(
                order.amount_total
                + order.fitit_installation_fee
                - order.fitit_down_payment
                - order.fitit_residual_payment,
                0.0,
            )
            finance_total = base * (1.0 + (order.fitit_interest_rate or 0.0) / 100.0)
            order.fitit_financed_base = base
            order.fitit_finance_total = finance_total
            order.fitit_finance_monthly_payment = (
                finance_total / order.fitit_financing_months
                if order.fitit_financing_months
                else 0.0
            )
            order.fitit_rental_monthly_payment = (
                base / order.fitit_rental_months if order.fitit_rental_months else 0.0
            )
            order.fitit_msi_monthly_payment = (
                order.amount_total / order.fitit_msi_months if order.fitit_msi_months else 0.0
            )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    fitit_equipment_model = fields.Char(
        string="Modelo Fit It",
        help="Modelo a imprimir en los reportes Fit It cuando difiere del producto.",
    )
    fitit_serial_number = fields.Char(string="Número de serie")
    fitit_service_date = fields.Date(string="Fecha de servicio")
    fitit_failure_report = fields.Text(string="Falla reportada")
    fitit_work_performed = fields.Text(string="Trabajo realizado")
