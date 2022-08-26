from collections.abc import Iterable
from contextlib import contextmanager

from manim import *
from manim import FadeIn

from .animations import GLOBAL_ANIMATION_BUFFER as BUFFER
from .colours import BACKGROUND, COLOUR

__all__ = ["MList", "Pointer"]


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
        kwargs.setdefault("color", COLOUR)
        super().__init__(**kwargs)
        self.data = value
        self.text = Text(str(value), color=COLOUR).move_to(self.get_center())
        self.add(self.text)
        self.selector = None
        self.colours = [BACKGROUND]

    def shade(self, colour):
        self.colours.append(colour)
        return self.animate.set_fill(colour, opacity=0.5, family=False)

    def unshade(self):
        self.colours.pop()
        return self.animate.set_fill(self.colours[-1], opacity=0, family=False)


class Pointer(Polygon, BufferedMobject):
    def __init__(self, side_length=1, colour=COLOUR, pointing=UP, **kwargs):
        points = (
            [-side_length / 4, 0, 0],
            [side_length / 4, 0, 0],
            [0, side_length / 8 * pointing[1], 0]
        )
        self.pointing = pointing
        kwargs.setdefault("color", colour)
        kwargs.setdefault("fill_color", colour)
        kwargs.setdefault("fill_opacity", 1.0)
        kwargs.setdefault("stroke_opacity", 1.0)
        super().__init__(*points, **kwargs)

    def point_to(self, elt, aligned_to=None):
        if aligned_to is None:
            aligned_to = elt
        BUFFER.push(
            lambda e=elt, a=aligned_to:
            (
                self.animate
                .next_to(e, -self.pointing)
                .align_to(a, -self.pointing)
                .shift(-self.pointing * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
            )
        )
