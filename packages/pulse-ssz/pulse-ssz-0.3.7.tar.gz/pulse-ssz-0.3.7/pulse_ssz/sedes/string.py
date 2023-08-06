from typing import Any

from pulse_ssz.exceptions import DeserializationError, SerializationError
from pulse_ssz.sedes.basic import BasicSedes


class String(BasicSedes[str, str]):
    def __init__(self) -> None:
        super().__init__(size=1)

    def serialize(self, v: str) -> bytes:
        value = int(v, 10)
        if value < 0:
            raise SerializationError(
                f"Can only serialize non-negative integers, got {value}"
            )

        try:
            return value.to_bytes(16, "little")
        except OverflowError:
            raise SerializationError(
                f"{value} is too large to be serialized in {16} bits"
            )

    def deserialize(self, data: bytes) -> str:
        if len(data) != self.size:
            raise DeserializationError(
                f"Cannot deserialize length {len(data)} byte-string as str{16}"
            )
        return str(int.from_bytes(data, "little"))

    def get_sedes_id(self) -> str:
        return self.__class__.__name__

    def __hash__(self) -> int:
        return hash((hash(String),))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, String)

string = String()