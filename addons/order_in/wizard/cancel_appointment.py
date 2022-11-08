from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class CancelAppointment(models.TransientModel):
    """cancel appointment"""

    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    appointment_id = fields.Many2one(
        "order.appointment",
        string="Appointment",
        domain=[("state", "=", "draft")],
    )
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    # todo tree view not update when cancel day from heder dropdown
    def action_cancel(self):
        """can cancel appointment before cancel_day param"""

        cancel_day = self.env["ir.config_parameter"].get_param("order_in.cancel_days")
        allow_date = self.appointment_id.booking_date + relativedelta.relativedelta(
            days=int(cancel_day)
        )
        if allow_date < self.date_cancel:
            raise ValidationError(_(f"can't cancel after {allow_date}"))
        self.appointment_id.state = "cancel"

    @api.model
    def default_get(self, field):
        """cancel appointment on self and not select appointment_id"""

        res = super().default_get(field)
        res["date_cancel"] = date.today()
        res["appointment_id"] = self.env.context.get("active_id")
        return res
