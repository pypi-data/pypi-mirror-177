from typing import Any

from ssz.exceptions import DeserializationError, SerializationError
from ssz.sedes.basic import BasicSedes


class String(BasicSedes[int, int]):
    def __init__(self, num_bits: int) -> None:
        if num_bits % 8 != 0:
            raise ValueError("Number of bits must be a multiple of 8")
        self.num_bits = num_bits
        super().__init__(num_bits // 8)

    def serialize(self, v: str) -> bytes:
        value = int(v, 10)
        if value < 0:
            raise SerializationError(
                f"Can only serialize non-negative integers, got {value}"
            )

        try:
            return value.to_bytes(self.size, "little")
        except OverflowError:
            raise SerializationError(
                f"{value} is too large to be serialized in {self.size * 8} bits"
            )

    def deserialize(self, data: bytes) -> str:
        if len(data) != self.size:
            raise DeserializationError(
                f"Cannot deserialize length {len(data)} byte-string as str{self.size*8}"
            )
        return str(int.from_bytes(data, "little"))

    def get_sedes_id(self) -> str:
        return f"{self.__class__.__name__}{self.num_bits}"

    def __hash__(self) -> int:
        return hash((hash(String), self.num_bits))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, String) and other.num_bits == self.num_bits

string = String(16)