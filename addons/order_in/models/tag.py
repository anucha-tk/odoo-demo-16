from odoo import models, fields, api


class Tag(models.Model):
    _name = "tag"
    _description = "Tag"

    name = fields.Char("Name")
    color = fields.Integer("Color")
    active = fields.Boolean("Active", default=True)

    _sql_constraints = [
        ("unique_tag_name", "unique (name)", "Name must be unique."),
    ]

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get("name"):
            default["name"] = self.name + " (copy)"

        return super(Tag, self).copy(default)
