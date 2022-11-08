# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """config order_in module"""

    _inherit = "res.config.settings"

    cancel_days = fields.Integer(
        string="Cancel Days", config_parameter="order_in.cancel_days"
    )
