from typing import TYPE_CHECKING, Iterable, Sequence, TypeVar

from eth_typing import Hash32

from pulse_ssz.hashable_structure import BaseResizableHashableStructure
from pulse_ssz.utils import mix_in_length

TElement = TypeVar("TElement")

if TYPE_CHECKING:
    from pulse_ssz.sedes import List


class HashableList(BaseResizableHashableStructure[TElement], Sequence[TElement]):
    @classmethod
    def from_iterable(
        cls, iterable: Iterable[TElement], sedes: "List[TElement, TElement]"
    ):
        return super().from_iterable_and_sedes(
            iterable, sedes, max_length=sedes.max_length
        )

    @property
    def hash_tree_root(self) -> Hash32:
        return mix_in_length(self.raw_root, len(self))
