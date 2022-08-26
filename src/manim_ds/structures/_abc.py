from abc import ABC

from manim import FadeIn, FadeOut, Mobject

from manim_ds.action import Action


class BufferedMobject(Mobject, ABC):
    def create(self):
        return Action(self, lambda: FadeIn(self))

    def uncreate(self):
        return Action(self, lambda: FadeOut(self))
