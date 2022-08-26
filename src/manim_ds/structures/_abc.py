from abc import ABC

from manim import FadeIn, FadeOut, Mobject

from manim_ds.action import Action


class BufferedMobject(Mobject, ABC):
    def create(self):
        return Action(lambda: FadeIn(self), value=self)

    def uncreate(self):
        return Action(lambda: FadeOut(self), value=self)
