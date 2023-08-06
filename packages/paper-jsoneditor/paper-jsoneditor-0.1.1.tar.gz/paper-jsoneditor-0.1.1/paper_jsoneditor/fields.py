from django.db import models
from django.db.models.fields.json import KeyTransform

from . import forms


class JSONField(models.JSONField):
    empty_values = [None, "", ()]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", dict)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": forms.JSONField,
                **kwargs,
            }
        )


class OrderedJSONField(JSONField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        # Some backends (SQLite at least) extract non-string values in their
        # SQL datatypes.
        if isinstance(expression, KeyTransform) and not isinstance(value, str):
            return value

        if isinstance(value, str):
            try:
                return json.loads(value, cls=self.decoder)
            except json.JSONDecodeError:
                pass

        return value

    def db_type(self, connection):
        if connection.vendor == "postgresql":
            return "json"

        internal_type = "TextField"
        data = self.db_type_parameters(connection)
        try:
            return connection.data_types[internal_type] % data
        except KeyError:
            return None
