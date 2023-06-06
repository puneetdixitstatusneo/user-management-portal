from marshmallow import Schema, ValidationError, fields, validates_schema
from marshmallow.validate import Length, OneOf


class DepartmentSchema(Schema):
    dept_name = fields.String(required=True)


class RoleSchema(Schema):
    role_name = fields.String(required=True)


class SignUpSchema(Schema):
    """
    In this schema we defined the required json for signup any user.
    """

    first_name = fields.String()
    last_name = fields.String()
    email_address = fields.Email(required=True)
    password = fields.String(required=True, validate=Length(min=8))  # noqa


class LogInSchema(Schema):
    """
    In this schema we defined the required json to log in any user.
    """

    username = fields.String()
    email = fields.Email()
    password = fields.String(required=True, validate=Length(min=8))  # noqa

    @validates_schema
    def validate_at_least_one_email_and_username(self, data, **kwargs):
        if not data.get("email") and not data.get("username"):
            raise ValidationError("At least one param is required from ['email', 'username']")


class UpdatePassword(Schema):
    """
    Required schema to update the password
    """

    old_password = fields.String(required=True)
    new_password = fields.String(required=True, validate=Length(min=8))  # noqa
