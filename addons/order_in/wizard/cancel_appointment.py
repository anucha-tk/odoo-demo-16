import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one("order.appointment", string="Appointment", domain=[("state", "=", "draft")])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError(_("cancellation isn't allow in the same day of booking"))
        self.appointment_id.state = "cancel"
        return

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointment, self).default_get(fields)
        res["date_cancel"] = datetime.date.today()
        res["appointment_id"] = self.env.context.get("active_id")
        return res
