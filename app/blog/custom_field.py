from django.db import models
from django.conf import settings
from django.db.models import fields


# MySQL unsigned integer (range 0 to 4294967295).
class UnsignedAutoField(models.AutoField):
    def db_type(self, connection):
        return 'integer UNSIGNED AUTO_INCREMENT'

    def rel_db_type(self, connection):
        return 'integer UNSIGNED'


# https://gist.github.com/taptorestart/47c1b2b8414a31e6d82c071ee2362232
# https://stackoverflow.com/a/51847760
class UnsignedIntegerField(fields.IntegerField):
    MAX_INT = 4294967295

    def db_type(self, connection):
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            return "integer UNSIGNED"
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            return 'integer'
        else:
            raise NotImplementedError

    def get_internal_type(self):
        return "UnsignedIntegerField"

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "min_value": 0,
                "max_value": self.MAX_INT,
                **kwargs,
            }
        )
