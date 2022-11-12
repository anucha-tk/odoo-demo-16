from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class OrderCustomer(models.Model):
    _name = "order.customer"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Customer"

    name = fields.Char(string="Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        inverse="_inverse_compute_age",
        tracking=True,
        search="_search_age",
    )
    address = fields.Char(string="Address", required=True, tracking=True)
    phone = fields.Char(string="Phone", required=True, tracking=True)
    email = fields.Char(string="Email", required=True, tracking=True)
    ref = fields.Char(string="Reference", tracking=True)
    active = fields.Boolean(string="Active", default=True)
    types = fields.Selection(
        [
            ("clinic", "Clinic"),
            ("hospital", "Hospital"),
            ("other", "Other"),
        ],
        string="customer_type",
    )
    tag_ids = fields.Many2many("tag", string="tags")
    image = fields.Image("Image")
    appointment_count = fields.Integer(
        compute="_compute_appointment_count",
        string="Appointment Count",
        store=True,
    )
    appointment_ids = fields.One2many(
        "order.appointment", "customer_id", string="Appointments"
    )
    parent = fields.Char("Parent")

    @staticmethod
    def _search_age(_, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [
            ("date_of_birth", ">=", start_of_year),
            ("date_of_birth", "<=", end_of_year),
        ]

    @api.depends("appointment_ids")
    def _compute_appointment_count(self):
        appointment_group = self.env["order.appointment"].read_group(
            domain=[], fields=[], groupby=["customer_id"]
        )
        for appointment in appointment_group:
            # get customer and appointment_count
            customer_id = appointment.get("customer_id")[0]
            appointment_count = appointment["customer_id_count"]
            # get customer record
            customer_rec = self.browse(customer_id)
            customer_rec.appointment_count = appointment_count
            self -= customer_rec
        self.appointment_count = 0

    @api.constrains("date_of_birth")
    def _constrains_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(
                    _("The entered date of birth is not acceptable !")
                )

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(
                    _("You can't delete this customer because it has appointments")
                )

    @api.model
    def create(self, vals):
        vals["ref"] = self.env["ir.sequence"].next_by_code("customer")
        return super(OrderCustomer, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get("ref"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("customer")
        return super(OrderCustomer, self).write(vals)

    @api.depends("date_of_birth")
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends("age")
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]

    def action_view_appointments(self):
        """show appointment_count form header button"""
        return {
            "name": _("Appointments"),
            "res_model": "order.appointment",
            "view_mode": "list,form",
            "context": {},
            "domain": [("customer_id", "=", self.id)],
            "target": "current",
            "type": "ir.actions.act_window",
        }
