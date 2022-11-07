from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OrderAppointment(models.Model):
    _name = "order.appointment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Order Appointment"
    _rec_name = "customer_id"

    customer_id = fields.Many2one("order.customer", string="Customer", required=True, ondelete="cascade")
    appointment_time = fields.Datetime(string="Appointment Time", required=True, default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", required=True, default=fields.Date.context_today)
    types = fields.Selection(string="customer_type", related="customer_id.types")
    ref = fields.Char(string="Reference", tracking=True)
    prescription = fields.Html(string="Prescription")
    state = fields.Selection(
        [("draft", "Draft"), ("in_consultation", "In Consultation"), ("done", "Done"), ("cancel", "Cancel")],
        default="draft",
        tracking=True,
        string="Status",
    )
    pharmacy_line_ids = fields.One2many("appointment.pharmacy.lines", "appointment_id", string="Pharmacy Lines")

    @api.onchange("customer_id")
    def _onchange_customer_id(self):
        self.ref = self.customer_id.ref

    def action_in_consultation(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = "in_consultation"

    def action_done(self):
        for rec in self:
            rec.state = "done"

    def action_cancel(self):
        action = self.env.ref("order_in.action_cancel_appointment").read()[0]
        return action

    def unlink(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError("You can delete appointment only draft status !")
        return super(OrderAppointment, self).unlink()


class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one("product.product", string="product", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1)
    price_unit = fields.Float(related="product_id.list_price", required=True)
    appointment_id = fields.Many2one("order.appointment", string="Appointment")
