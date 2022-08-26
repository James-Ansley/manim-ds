from manim import DEFAULT_MOBJECT_TO_MOBJECT_BUFFER, FadeIn, FadeOut, Polygon, \
    UP

from manim_ds.action import Action
from manim_ds.config import CONFIG
from manim_ds.scene import GLOBAL_ANIMATION_BUFFER as BUFFER


class Pointer(Polygon):
    def __init__(self, side_length=1, pointing=UP, **kwargs):
        points = (
            [-side_length / 4, 0, 0],
            [side_length / 4, 0, 0],
            [0, side_length / 8 * pointing[1], 0]
        )
        self.pointing = pointing
        kwargs.setdefault("color", CONFIG["colour"])
        kwargs.setdefault("fill_color", CONFIG["colour"])
        kwargs.setdefault("fill_opacity", 1.0)
        kwargs.setdefault("stroke_opacity", 1.0)
        super().__init__(*points, **kwargs)

    def create(self):
        return Action(self, lambda: FadeIn(self))

    def uncreate(self):
        return Action(self, lambda: FadeOut(self))

    def point_to(self, elt, aligned_to=None):
        if aligned_to is None:
            aligned_to = elt
        return Action(
            None,
            lambda e=elt, a=aligned_to:
            (
                self.animate
                .next_to(e, -self.pointing)
                .align_to(a, -self.pointing)
                .shift(-self.pointing * DEFAULT_MOBJECT_TO_MOBJECT_BUFFER)
            )
        )
