class MaxMidRegistry:
    def __init__(self) -> None:
        self._mid_to_int: dict[str, int] = {}
        self._int_to_mid: dict[int, str] = {}

    @property
    def mid_to_int(self) -> dict[str, int]:
        return self._mid_to_int

    def register_mid(self, mid: str) -> int:
        if mid in self._mid_to_int:
            return self._mid_to_int[mid]
        int_id = hash(mid) & 0x7FFFFFFF
        while int_id in self._int_to_mid and self._int_to_mid[int_id] != mid:
            int_id = (int_id + 1) & 0x7FFFFFFF
        self._mid_to_int[mid] = int_id
        self._int_to_mid[int_id] = mid
        return int_id

    def int_to_mid(self, int_id: int) -> str:
        return self._int_to_mid.get(int_id, str(int_id))
