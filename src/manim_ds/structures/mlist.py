from collections.abc import Iterable
from contextlib import contextmanager

from manim import *
from manim import FadeIn

from ..config import CONFIG
from ..scene.global_buffer import GLOBAL_ANIMATION_BUFFER as BUFFER

__all__ = ["MList"]


class BufferedMobject(Mobject):
    def create(self, animation=FadeIn):
        BUFFER.push(lambda: animation(self))
        return self

    def uncreate(self, animation=FadeOut):
        BUFFER.push(lambda: animation(self))
        return self

    def push(self, *animations):
        BUFFER.push(*animations)
        return self


def _swap_mobjects(e1, e2):
    return e1.animate.shift(e2.get_center() - e1.get_center())


class MList(VGroup, BufferedMobject):
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        self.arrange_submobjects(buff=0)

    @classmethod
    def from_iterable(cls, values: Iterable, **kwargs):
        elements = (_ListElement(v) for v in values)
        return cls(*elements, **kwargs)

    def shade(self, idx, colour):
        elt = self[idx]
        BUFFER.push(lambda e=elt, c=colour: e.shade(colour))
        return elt.data

    def unshade(self, idx):
        elt = self[idx]
        BUFFER.push(elt.deactivate)

    def compare(self, cmp, i, j):
        elt1, elt2 = self[i], self[j]
        self.push(
            lambda: elt1.shade(ORANGE).shift(UP),
            lambda: elt2.shade(ORANGE).shift(UP),
        )
        return cmp(elt1.data, elt2.data)

    @contextmanager
    def comparing(self, cmp, i, j):
        comparing = i, j
        try:
            yield self.compare(cmp, *comparing)
        finally:
            self.uncompare(*comparing)

    def uncompare(self, i, j):
        elt1, elt2 = self[i], self[j]
        self.push(
            lambda: elt1.unshade().shift(DOWN),
            lambda: elt2.unshade().shift(DOWN),
        )

    def swap(self, i, j):
        elt1, elt2 = self[i], self[j]
        self.push(
            lambda e1=elt1, e2=elt2: _swap_mobjects(e1, e2),
            lambda e2=elt2, e1=elt1: _swap_mobjects(e2, e1),
        )
        self[i], self[j] = self[j], self[i]


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
        return self.animate.set_fill(colour, family=False)

    def unshade(self):
        return self.animate.set_fill(self.background, family=False)
