import magic
import types

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData


# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.readthedocs.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)


def method_callback_wrapper (original_method, callbacks):
    def wrapper (self, *args, **kwargs):
        value = original_method(*args, **kwargs)
        for callback in callbacks:
            callback(value)
        return value
    return types.MethodType(
        wrapper, original_method.__self__)


class MagicBufferProcessor (object):

    def __init__ (self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.type_ = None

    def process (self, value):
        if not self.type_:
            self.type_ = magic.from_buffer(value, *self.args, **self.kwargs)
