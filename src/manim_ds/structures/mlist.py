from collections.abc import Iterable

from manim import *
from manim import FadeIn

from ..action import Action
from ..config import CONFIG

__all__ = ["MList"]


def _swap_mobjects(e1, e2):
    return e1.animate.shift(e2.get_center() - e1.get_center())


class MList(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.arrange_submobjects(buff=0)

    def create(self):
        return Action(self, lambda: FadeIn(self))

    def uncreate(self):
        return Action(self, lambda: FadeOut(self))

    @classmethod
    def from_iterable(cls, values: Iterable, **kwargs):
        elements = (_ListElement(v) for v in values)
        return cls(*elements, **kwargs)

    def compare(self, cmp, i, j):
        elt1, elt2 = self[i], self[j]
        return Action(
            cmp(elt1.data, elt2.data),
            elt1.shade(ORANGE),
            elt2.shade(ORANGE),
        ).then("shift", UP)

    def uncompare(self, i, j):
        elt1, elt2 = self[i], self[j]
        return Action(
            None,
            elt1.unshade(),
            elt2.unshade(),
        ).then("shift", DOWN)

    def swap(self, i, j):
        elt1, elt2 = self[i], self[j]
        a = Action(
            None,
            lambda e1=elt1, e2=elt2: _swap_mobjects(e1, e2),
            lambda e2=elt2, e1=elt1: _swap_mobjects(e2, e1),
        )
        self[i], self[j] = self[j], self[i]
        return a


class _ListElement(Square):
    def __init__(self, value, **kwargs):
        kwargs.setdefault("side_length", 1.0)
        kwargs.setdefault("color", CONFIG["colour"])
        kwargs.setdefault("fill_color", CONFIG["background"])
        kwargs.setdefault("fill_opacity", 0.5)
        super().__init__(**kwargs)
        self.data = value
        self.add(
            Text(str(value), color=kwargs["color"])
            .move_to(self.get_center())
        )
        self.background = kwargs["fill_color"]

    def shade(self, colour):
        return Action(
            None,
            lambda: self.animate.set_fill(colour, family=False)
        )

    def unshade(self):
        return Action(
            None,
            lambda: self.animate.set_fill(self.background, family=False)
        )
