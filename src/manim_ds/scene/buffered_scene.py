from itertools import chain

from manim import Scene, config

from manim_ds.config import CONFIG


class BufferedScene(Scene):
    def __init__(self):
        self.buffer = []
        super().__init__()

    def do(self, action):
        self.buffer.append(action.animations)
        return action.value

    def do_all(self, *actions):
        self.buffer.append(chain(*(a.animations for a in actions)))
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

    def construct(self):
        self.camera.background_color = CONFIG["background"]
        for animations in self.buffer:
            self.play(*(a() for a in animations))
