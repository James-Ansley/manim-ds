from manim import Scene, config

from manim_ds.config import CONFIG
from manim_ds.scene.global_buffer import GLOBAL_ANIMATION_BUFFER


class BufferedScene(Scene):
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
        for animations in GLOBAL_ANIMATION_BUFFER:
            self.play(*animations)
