from itertools import chain

from manim import Scene, config

from manim_ds.action import Action
from manim_ds.config import CONFIG


def _hoist(action):
    if not isinstance(action, Action):
        action = Action(action)
    return action


class ActionScene(Scene):
    def setup(self):
        self.camera.background_color = CONFIG["background"]

    def do(self, action):
        action = _hoist(action)
        self.play(*action.animations)
        return action.value

    def do_all(self, *actions):
        animations = chain(*(_hoist(a).animations for a in actions))
        self.play(*animations)
        return (a.value for a in actions)

    def set_size(self, width, height):
        pixel_width = CONFIG["pixelsPerUnit"] * width
        pixel_height = CONFIG["pixelsPerUnit"] * height
        config.pixel_width = pixel_width
        config.pixel_height = pixel_height
        self.camera.frame_width = width
        self.camera.frame_height = height
        self.camera.pixel_width = pixel_width
        self.camera.pixel_height = pixel_height
