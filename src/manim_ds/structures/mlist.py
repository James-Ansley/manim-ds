from manim import *

from manim_ds.action import Action
from manim_ds.config import CONFIG
from ._abc import ActionMobject

__all__ = ["MList"]


class MList(VGroup, ActionMobject):
    def __init__(self, values, **kwargs):
        elements = (_ListElement(v) for v in values)
        super().__init__(*elements, **kwargs)
        self.arrange_submobjects(buff=0)

    def compare(self, cmp, i, j):
        elt1, elt2 = self[i], self[j]
        return Action(
            elt1.shade(ORANGE),
            elt2.shade(ORANGE),
            value=cmp(elt1.data, elt2.data)
        ).then("shift", UP)

    def uncompare(self, i, j):
        elt1, elt2 = self[i], self[j]
        return Action(elt1.unshade(), elt2.unshade()).then("shift", DOWN)

    def swap(self, i, j):
        elt1, elt2 = self[i], self[j]
        self[i], self[j] = self[j], self[i]
        return Action(elt1.shift_to(elt2), elt2.shift_to(elt1))


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
        return Action(self.animate.set_fill(colour, family=False))

    def unshade(self):
        return Action(self.animate.set_fill(self.background, family=False))

    def shift_to(self, target):
        return Action(
            self.animate.shift(target.get_center() - self.get_center()),
        )
