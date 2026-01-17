
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CompanyLease(models.Model):
    _name = "company.lease"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Company Lease"
    _rec_name = "contract_number"
    _order = "end_date asc"
    

    region = fields.Char(string="Name of residence/office", required=True, tracking=True)

    unit_type = fields.Selection(
        [
            ("office", "Office"),
            ("contractors_office", "Contractors Office"),
            ("customer_service_office", "Customer Service Office"),
            ("villa", "Villa"),
            ("contractors_villa", "Contractors Villa"),
            ("customer_service_villa", "Customer Service Villa"),
            ("apartment", "Apartment"),
            ("contractors_apartment", "Contractors Apartment"),
            ("customer_service_apartment", "Customer Service Apartment"),
        ],
        string="Unit Type",
        required=True,
        default="office",
        tracking=True,
    )

    partner_id = fields.Many2one("institution.master", string="Office / Company", required=True, tracking=True)

    establishment_representative = fields.Selection(
        [
            ("abu_nayef", "ابو نايف"),
            ("abu_saad", "ابو سعد"),
            ("fahad_zain", "فهاد زاين"),
            ("mohammed_alloush", "محمد علوش"),
            ("bari_zain", "باري زاين"),
            ("noura_bari", "نوره باري"),
            ("noura_zain", "نوره زاين"),
            ("miznah_zain", "مزنة زاين"),
            ("ryoof_alloush", "ريوف علوش"),
            ("nouf_zain", "نوف زاين"),
            ("rajsaa_alloush", "رجساء علوش"),
        ],
        string="Establishment Representative",
        tracking=True,
    )

    contract_number = fields.Char(string="Contract Number", required=True, index=True, tracking=True)
    start_date = fields.Date(string="Start Date", required=True, tracking=True)
    end_date = fields.Date(string="End Date", required=True, tracking=True)

    installments_per_year = fields.Integer(string="Installments per Year", default=1, tracking=True)

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )

    total_rental_amount = fields.Monetary(string="Total Rental Amount", required=True, default=0.0, tracking=True)
    amount_paid = fields.Monetary(
        string="Amount Paid",
        compute="_compute_amounts",
        store=True,
        readonly=True,
    )
    remaining_balance = fields.Monetary(
        string="Remaining Balance",
        compute="_compute_amounts",
        store=True,
        readonly=True,
    )

    landlord_bank_account = fields.Char(string="Bank Number", tracking=True)
    notes = fields.Text(string="Notes (VAT/Remarks)", tracking=True)

    days_to_expiry = fields.Integer(string="Days to Expiry", compute="_compute_expiry", store=True)
    renewal_alert = fields.Boolean(string="Renewal Alert", compute="_compute_expiry", store=True)

    lease_status = fields.Selection(
        [
            ("active", "Active"),
            ("expiring", "Expiring (< 3 months)"),
            ("expired", "Expired"),
        ],
        string="Lease Status",
        compute="_compute_expiry",
        store=True,
        index=True,
        tracking=True,
    )

    # ✅ Payments lines (real-life tracking)
    payment_line_ids = fields.One2many(
        "company.lease.payment",
        "lease_id",
        string="Payments",
        copy=False,
    )

    _sql_constraints = [
        ("contract_number_unique", "unique(contract_number)", "Contract Number must be unique."),
    ]

    @api.depends("total_rental_amount", "payment_line_ids.amount")
    def _compute_amounts(self):
        for rec in self:
            paid = sum(rec.payment_line_ids.mapped("amount"))
            rec.amount_paid = paid
            rec.remaining_balance = (rec.total_rental_amount or 0.0) - paid

    @api.depends("end_date")
    def _compute_expiry(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if not rec.end_date:
                rec.days_to_expiry = 0
                rec.renewal_alert = False
                rec.lease_status = "active"
                continue

            delta = (rec.end_date - today).days
            rec.days_to_expiry = delta

            if delta < 0:
                rec.renewal_alert = False
                rec.lease_status = "expired"
            elif delta < 90:
                rec.renewal_alert = True
                rec.lease_status = "expiring"
            else:
                rec.renewal_alert = False
                rec.lease_status = "active"

    @api.constrains("total_rental_amount", "payment_line_ids")
    def _check_no_overpayment(self):
        for rec in self:
            paid = sum(rec.payment_line_ids.mapped("amount"))
            if rec.total_rental_amount and paid > rec.total_rental_amount:
                raise ValidationError(_(
                    "Total paid (%(paid)s) cannot be greater than total rental amount (%(total)s).",
                    paid=paid,
                    total=rec.total_rental_amount,
                ))


class CompanyLeasePayment(models.Model):
    _name = "company.lease.payment"
    _description = "Lease Payment"
    _order = "payment_date desc, id desc"

    lease_id = fields.Many2one("company.lease", string="Lease", required=True, ondelete="cascade", tracking=True)

    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today, required=True)
    amount = fields.Monetary(string="Amount", required=True, default=0.0, tracking=True)

    currency_id = fields.Many2one(
        related="lease_id.currency_id",
        store=True,
        readonly=True,
    )

    # paid_by = fields.Many2one(
    #     "res.users",
    #     string="Paid By",
    #     default=lambda self: self.env.user,
    #     required=True,
    #     readonly=True,
    # )

    # reference = fields.Char(string="Reference")
    # note = fields.Text(string="Notes")

    receipt_attachment_ids = fields.Many2many(
        "ir.attachment",
        "company_lease_payment_attachment_rel",
        "payment_id",
        "attachment_id",
        string="Receipts",
        help="Upload transfer receipt(s) for this payment.",
    )

    installment_number = fields.Char(string="Installment Number", default="1", tracking=True)
    note = fields.Text(string="Notes", tracking=True)

    







