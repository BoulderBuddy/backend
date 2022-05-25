from decimal import Decimal
from enum import Enum, IntEnum
from typing import Type

from sqlalchemy import Integer, Numeric, TypeDecorator
from sqlalchemy.engine.default import DefaultDialect


# Problem: SQLite does not support native decimals
# This decorator will user native decimals if the dialect supports it
# Otherwise it will convert decimals into integers for database storage
class CustomNumeric(TypeDecorator):
    impl = Numeric

    def __init__(self, *arg, **kw):
        TypeDecorator.__init__(self, *arg, **kw)
        self.scale = self.impl.scale
        self.multiplier = 10**self.scale

    def load_dialect_impl(self, dialect: DefaultDialect):
        if dialect.supports_native_decimal:
            return dialect.type_descriptor(self.impl)
        else:
            return dialect.type_descriptor(Integer)

    def process_bind_param(self, value, dialect: DefaultDialect):
        # e.g. value = Column(CustomNumeric(2)) means a value such as
        # Decimal('12.34') will be converted to 1234
        if value is not None and not dialect.supports_native_decimal:
            # temp: Decimal =
            # if temp > 9223372036854775807:
            #     # TODO verfiy that this is the case?
            #     raise OverflowError("Value would cause overflow")
            value = int(Decimal(value) * self.multiplier)
        return value

    def process_result_value(self, value, dialect: DefaultDialect):
        # e.g. Integer 1234 will be converted to Decimal('12.34'),
        # when query takes place.
        if value is not None and not dialect.supports_native_decimal:
            value = Decimal(value) / self.multiplier
        return value


class CustomEnum(TypeDecorator):
    impl = Integer

    def __init__(self, enum: Type[IntEnum]):
        TypeDecorator.__init__(self)
        self.enum_class = enum

    def process_bind_param(self, value: Enum | None, dialect: DefaultDialect):
        if value is not None:
            value = self.enum_class[value.value].value
        return value

    def process_result_value(self, value: int, dialect: DefaultDialect):
        if value is not None:
            value = self.enum_class(value).name
        return value
