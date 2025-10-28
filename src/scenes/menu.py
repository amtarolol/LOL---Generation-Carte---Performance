# scenes/menu.py
import pygame
from core.scene import Scene

class MenuScene(Scene):
    def on_enter(self, **kwargs):
        self.W, self.H = self.screen.get_size()
        self.title_font = pygame.font.SysFont(None, 72)
        self.ui_font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 28)

        self.nb_buffs = 10
        self.min_buffs, self.max_buffs = 1, 100
        self.start_pt = None
        self.end_pt = None

        # UI
        self.minus_rect = pygame.Rect(self.W//2 - 200, self.H//2 + 40, 80, 60)
        self.plus_rect  = pygame.Rect(self.W//2 + 120, self.H//2 + 40, 80, 60)
        self.start_rect = pygame.Rect(self.W//2 - 160, self.H//2 + 140, 320, 64)
        self.value_rect = pygame.Rect(self.W//2 - 100, self.H//2 + 40, 200, 60)

    # UI helpers
    def draw_button(self, rect, text, hover=False):
        color_bg = (70, 70, 80) if not hover else (100, 100, 120)
        pygame.draw.rect(self.screen, color_bg, rect, border_radius=12)
        pygame.draw.rect(self.screen, (150, 150, 170), rect, 2, border_radius=12)
        label = self.ui_font.render(text, True, (230, 230, 240))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def draw_point(self, p, color):
        pygame.draw.circle(self.screen, color, p, 8)
        pygame.draw.circle(self.screen, (255, 255, 255), p, 8, 2)

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.request_quit = True
            elif e.key in (pygame.K_RIGHT, pygame.K_KP_PLUS):
                self.nb_buffs = min(self.max_buffs, self.nb_buffs + 1)
            elif e.key in (pygame.K_LEFT, pygame.K_KP_MINUS):
                self.nb_buffs = max(self.min_buffs, self.nb_buffs - 1)
            elif e.key == pygame.K_r:
                self.start_pt, self.end_pt = None, None
            elif e.key == pygame.K_RETURN and self.start_pt and self.end_pt:
                from scenes.game import GameScene
                self.switch_to(GameScene,
                               nb_buffs=self.nb_buffs,
                               start_pt=self.start_pt,
                               end_pt=self.end_pt)

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.minus_rect.collidepoint(e.pos):
                self.nb_buffs = max(self.min_buffs, self.nb_buffs - 1)
            elif self.plus_rect.collidepoint(e.pos):
                self.nb_buffs = min(self.max_buffs, self.nb_buffs + 1)
            elif self.start_rect.collidepoint(e.pos):
                if self.start_pt and self.end_pt:
                    from scenes.game import GameScene
                    self.switch_to(GameScene,
                                   nb_buffs=self.nb_buffs,
                                   start_pt=self.start_pt,
                                   end_pt=self.end_pt)
            else:
                # clic libre pour placer les points
                if self.start_pt is None:
                    self.start_pt = e.pos
                elif self.end_pt is None:
                    self.end_pt = e.pos
                else:
                    # remplace le plus proche
                    sx, sy = self.start_pt
                    ex, ey = self.end_pt
                    mx, my = e.pos
                    if (mx - sx)**2 + (my - sy)**2 <= (mx - ex)**2 + (my - ey)**2:
                        self.start_pt = e.pos
                    else:
                        self.end_pt = e.pos

    def update(self, dt): pass

    def draw(self):
        self.screen.fill((18, 19, 23))

        title = self.title_font.render("Configurer la partie", True, (240, 240, 255))
        self.screen.blit(title, title.get_rect(center=(self.W//2, 120)))
        sub = self.ui_font.render("Clique pour définir la lane : début puis fin", True, (210, 210, 230))
        self.screen.blit(sub, sub.get_rect(center=(self.W//2, 190)))

        # Preview lane
        if self.start_pt:
            self.draw_point(self.start_pt, (0, 200, 255))
        if self.end_pt:
            self.draw_point(self.end_pt, (255, 140, 0))
        if self.start_pt and self.end_pt:
            pygame.draw.line(self.screen, (120, 200, 255), self.start_pt, self.end_pt, 3)

        # Controls nb buffs
        label_b = self.ui_font.render("Nombre de buffs :", True, (230, 230, 240))
        self.screen.blit(label_b, label_b.get_rect(center=(self.W//2, self.H//2 + 10)))

        self.draw_button(self.minus_rect, "–", self.minus_rect.collidepoint(pygame.mouse.get_pos()))
        self.draw_button(self.plus_rect,  "+", self.plus_rect.collidepoint(pygame.mouse.get_pos()))

        pygame.draw.rect(self.screen, (40, 42, 50), self.value_rect, border_radius=12)
        pygame.draw.rect(self.screen, (120, 120, 140), self.value_rect, 2, border_radius=12)
        label_val = self.ui_font.render(str(self.nb_buffs), True, (255, 255, 255))
        self.screen.blit(label_val, label_val.get_rect(center=self.value_rect.center))

        # Start
        ready = self.start_pt and self.end_pt
        self.draw_button(self.start_rect, "Générer" if ready else "Place les 2 points",
                         self.start_rect.collidepoint(pygame.mouse.get_pos()))

        hint = self.small_font.render("Clic: fixer un point • R: reset • Entrée: valider • Échap: quitter",
                                      True, (170, 170, 190))
        self.screen.blit(hint, hint.get_rect(center=(self.W//2, self.H - 40)))
