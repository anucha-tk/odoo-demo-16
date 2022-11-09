from odoo import models, fields, api


class Operation(models.Model):
    """Operation"""

    _name = "operation"
    _description = "Operation"
    _log_access = False

    doctor_id = fields.Many2one("res.users", string="Doctor")
    operation_name = fields.Char(string="Name")
    reference_record = fields.Reference(
        selection=[
            ("order.customer", "Customer"),
            ("order.appointment", "Appointment"),
        ],
        string="Record",
    )

    @api.model
    def name_create(self, name):
        """override create function"""
        print(name)
        return self.create({"operation_name": name}).name_get()[0]
