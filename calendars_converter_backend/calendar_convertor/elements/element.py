from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Element:
    top: int
    bottom: int
    left: int
    right: int

    def contains(self, other_element: "Element", ignore_left: bool = False, buffer: int = 0) -> bool:
        if not ignore_left and other_element.left + buffer < self.left:
            return False
        if other_element.top + buffer < self.top:
            return False
        if other_element.right - buffer > self.right:
            return False
        if other_element.bottom - buffer > self.bottom:
            return False
        return True
