# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cancel_days = fields.Integer(string="Cancel Days", config_parameter="order_in.cancel_days")
