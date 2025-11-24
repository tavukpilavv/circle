from marshmallow import Schema, fields, validates_schema, ValidationError, pre_load
from utils.helpers import sanitize_html


class PaginationSchema(Schema):
    page = fields.Int(load_default=1, validate=lambda x: x > 0)
    per_page = fields.Int(load_default=None)


class EventFilterSchema(PaginationSchema):
    campus = fields.Str(load_default=None)
    q = fields.Str(load_default=None)
    tag = fields.Str(load_default=None)
    status = fields.Str(load_default=None)
    start_from = fields.DateTime(load_default=None)
    end_to = fields.DateTime(load_default=None)


class EventCreateSchema(Schema):
    club_id = fields.Str(required=True)
    venue_id = fields.Str(load_default=None)
    visibility_type_id = fields.Str(load_default=None)
    title = fields.Str(required=True)
    description = fields.Str(load_default=None)
    start_at = fields.DateTime(required=True)
    end_at = fields.DateTime(required=True)
    capacity = fields.Int(load_default=None)
    banner_url = fields.Str(load_default=None)
    tag_ids = fields.List(fields.Str(), load_default=list)

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data.get("start_at") and data.get("end_at") and data["end_at"] <= data["start_at"]:
            raise ValidationError("end_at must be after start_at", "end_at")

    @pre_load
    def sanitize(self, data, **kwargs):
        if data.get("description"):
            data["description"] = sanitize_html(data["description"])
        return data


class SignupSchema(Schema):
    user_id = fields.Str(load_default=None)
    email = fields.Email(required=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class ClubSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(load_default=None)
