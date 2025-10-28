# core/scene.py
import pygame

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.is_done = False
        self.request_quit = False

    # Hooks
    def on_enter(self, **kwargs): pass
    def on_exit(self): pass

    # Cycle
    def handle_event(self, event): pass
    def update(self, dt): pass
    def draw(self): pass

    # Transitions
    def switch_to(self, scene_cls, **kwargs):
        self.next_scene = (scene_cls, kwargs)
        self.is_done = True

