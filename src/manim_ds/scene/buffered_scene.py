from itertools import chain

from manim import Scene, config

from manim_ds.action import Action
from manim_ds.config import CONFIG


def _hoist(action):
    if not isinstance(action, Action):
        action = Action(action, value=None)
    return action


class BufferedScene(Scene):
    def do(self, action):
        action = _hoist(action)
        self.play(*(a() for a in action.animations))
        return action.value

    def do_all(self, *actions):
        animations = chain(*(_hoist(a).animations for a in actions))
        self.play(*(a() for a in animations))

    def set_size(self, width, height):
        pixel_width = CONFIG["pixelsPerUnit"] * width
        pixel_height = CONFIG["pixelsPerUnit"] * height
        config.pixel_width = pixel_width
        config.pixel_height = pixel_height
        self.camera.frame_width = width
        self.camera.frame_height = height
        self.camera.pixel_width = pixel_width
        self.camera.pixel_height = pixel_height
