from abc import ABC

from manim import FadeIn, FadeOut, Mobject

from manim_ds.action import Action


class ActionMobject(Mobject, ABC):
    def create(self):
        return Action(FadeIn(self), value=self)

    def uncreate(self):
        return Action(FadeOut(self), value=self)
