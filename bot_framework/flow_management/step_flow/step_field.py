from __future__ import annotations

from typing import Any, get_args

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class StepField[T]:
    __slots__ = ("_value", "_skipped", "_skippable")

    def __init__(
        self,
        value: T | None = None,
        *,
        skipped: bool = False,
        skippable: bool = False,
    ) -> None:
        self._value = value
        self._skipped = skipped
        self._skippable = skippable

    @property
    def value(self) -> T | None:
        return self._value

    @value.setter
    def value(self, val: T | None) -> None:
        self._value = val
        if val is not None:
            self._skipped = False

    @property
    def skipped(self) -> bool:
        return self._skipped

    @property
    def skippable(self) -> bool:
        return self._skippable

    @property
    def completed(self) -> bool:
        return self._value is not None or self._skipped

    def skip(self) -> None:
        self._skipped = True

    def __bool__(self) -> bool:
        return self.completed

    def __repr__(self) -> str:
        if self._skipped:
            return "StepField(skipped)"
        return f"StepField({self._value!r})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StepField):
            return self._value == other._value and self._skipped == other._skipped
        return NotImplemented

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        args = get_args(source_type)
        inner_type = args[0] if args else Any

        inner_schema = handler.generate_schema(inner_type)

        def serialize(field: StepField[Any]) -> dict[str, Any]:
            return {
                "value": field._value,
                "skipped": field._skipped,
                "skippable": field._skippable,
            }

        dict_schema = core_schema.typed_dict_schema(
            {
                "value": core_schema.typed_dict_field(
                    core_schema.nullable_schema(inner_schema),
                    required=False,
                ),
                "skipped": core_schema.typed_dict_field(
                    core_schema.bool_schema(),
                    required=False,
                ),
                "skippable": core_schema.typed_dict_field(
                    core_schema.bool_schema(),
                    required=False,
                ),
            },
        )

        def from_dict(data: dict[str, Any]) -> StepField[Any]:
            return StepField(
                value=data.get("value"),
                skipped=data.get("skipped", False),
                skippable=data.get("skippable", False),
            )

        def from_raw_value(data: Any) -> StepField[Any]:
            return StepField(value=data)

        from_dict_schema = core_schema.chain_schema([
            dict_schema,
            core_schema.no_info_plain_validator_function(from_dict),
        ])

        from_value_schema = core_schema.chain_schema([
            core_schema.nullable_schema(inner_schema),
            core_schema.no_info_plain_validator_function(from_raw_value),
        ])

        from_instance_schema = core_schema.is_instance_schema(StepField)

        return core_schema.union_schema(
            [
                from_instance_schema,
                from_dict_schema,
                from_value_schema,
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize,
                info_arg=False,
            ),
        )
