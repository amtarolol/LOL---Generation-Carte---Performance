# scenes/menu.py — version avec choix d'algo (grid/random) et seed optionnelle
import pygame
from core.scene import Scene

class MenuScene(Scene):
    def on_enter(self, **kwargs):
        self.W, self.H = self.screen.get_size()
        self.title_font = pygame.font.SysFont(None, 72)
        self.ui_font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 28)

        # Etats
        self.nb_buffs_str = "10"      # texte saisi (string)
        self.nb_bushes_str = "30"
        self.nb_min, self.nb_max = 0, 9999
        self.algorithm = "grid"        # "grid" ou "random"
        self.seed_str = ""             # vide => pas de seed (aléatoire)
        self.start_pt = None
        self.end_pt = None

        # Champs de saisie
        field_w, field_h = 200, 56
        gap = 16
        center_x = self.W // 2

        self.buffs_label_pos = (center_x - 220, self.H // 2 - (field_h + gap))
        self.bushes_label_pos = (center_x - 220, self.H // 2 + 10)

        self.buffs_rect  = pygame.Rect(center_x - field_w//2, self.H // 2 - (field_h + gap), field_w, field_h)
        self.bushes_rect = pygame.Rect(center_x - field_w//2, self.H // 2 + 10,               field_w, field_h)

        # Ligne Algo + Seed
        algo_y = self.H // 2 + 75
        seed_y = algo_y + 56 + 12

        # Boutons algo
        btn_w, btn_h = 120, 44
        self.grid_btn_rect   = pygame.Rect(center_x - btn_w - 8, algo_y, btn_w, btn_h)
        self.random_btn_rect = pygame.Rect(center_x + 8,          algo_y, btn_w, btn_h)

        # Champ seed
        seed_w, seed_h = 200, 44
        self.seed_rect = pygame.Rect(center_x - seed_w//2, seed_y, seed_w, seed_h)

        # Bouton démarrer
        self.start_rect = pygame.Rect(center_x - 160, self.H // 2 + 120 + 90, 320, 64)

        # Focus (None | "buffs" | "bushes" | "seed")
        self.focus = None

    # UI helpers
    def _draw_input(self, rect, text, placeholder, focused=False):
        bg = (50, 54, 64) if not focused else (60, 64, 76)
        border_col = (140, 140, 160) if not focused else (100, 180, 255)
        pygame.draw.rect(self.screen, bg, rect, border_radius=10)
        pygame.draw.rect(self.screen, border_col, rect, 2, border_radius=10)

        shown = text if text != "" else placeholder
        col = (255, 255, 255) if text != "" else (190, 190, 200)
        label = self.ui_font.render(shown, True, col)
        self.screen.blit(label, label.get_rect(center=rect.center))

        # Curseur
        if focused:
            t = (pygame.time.get_ticks() // 500) % 2
            if t == 0:
                cursor_x = rect.centerx + label.get_width()//2 + 6
                pygame.draw.line(self.screen, (220, 220, 240),
                                 (cursor_x, rect.top + 10),
                                 (cursor_x, rect.bottom - 10), 2)

    def _draw_button(self, rect, text, hover=False):
        color_bg = (70, 70, 80) if not hover else (100, 100, 120)
        pygame.draw.rect(self.screen, color_bg, rect, border_radius=12)
        pygame.draw.rect(self.screen, (150, 150, 170), rect, 2, border_radius=12)
        label = self.ui_font.render(text, True, (230, 230, 240))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_point(self, p, color):
        pygame.draw.circle(self.screen, color, p, 8)
        pygame.draw.circle(self.screen, (255, 255, 255), p, 8, 2)

    def _draw_toggle(self, rect, text, active, hover=False):
        bg = (60, 68, 80) if not active else (35, 140, 90)
        if hover and not active:
            bg = (80, 90, 105)
        pygame.draw.rect(self.screen, bg, rect, border_radius=10)
        pygame.draw.rect(self.screen, (180, 180, 200), rect, 2, border_radius=10)
        label = self.ui_font.render(text, True, (255,255,255))
        self.screen.blit(label, label.get_rect(center=rect.center))

    def _draw_label_left(self, pos, text):
        lbl = self.ui_font.render(text, True, (230,230,240))
        r = lbl.get_rect(midleft=pos)
        self.screen.blit(lbl, r)

    def _parse_int_clamped(self, s):
        if s == "" or s is None:
            return None
        try:
            v = int(s)
        except ValueError:
            return None
        return max(self.nb_min, min(self.nb_max, v))

    def _parse_optional_int(self, s):
        if s is None or s == "":
            return None
        try:
            return int(s)
        except ValueError:
            return None

    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.request_quit = True
                return

            # Entrée : valider si prêt
            if e.key == pygame.K_RETURN:
                nb_buffs  = self._parse_int_clamped(self.nb_buffs_str)
                nb_bushes = self._parse_int_clamped(self.nb_bushes_str)
                seed      = self._parse_optional_int(self.seed_str)
                if self.start_pt and self.end_pt and (nb_buffs is not None) and (nb_bushes is not None):
                    from scenes.game import GameScene
                    self.switch_to(
                        GameScene,
                        nb_buffs=nb_buffs,
                        nb_bushes=nb_bushes,
                        start_pt=self.start_pt,
                        end_pt=self.end_pt,
                        placement=self.algorithm,
                        seed=seed,
                    )
                return

            # Saisie numérique / backspace sur champ focus
            if self.focus is not None:
                target_map = {
                    "buffs":  "nb_buffs_str",
                    "bushes": "nb_bushes_str",
                    "seed":   "seed_str",
                }
                target = target_map[self.focus]
                if e.key == pygame.K_BACKSPACE:
                    setattr(self, target, getattr(self, target)[:-1])
                elif e.key == pygame.K_MINUS and self.focus == "seed":
                    curr = getattr(self, target)
                    if len(curr) < 9 and len(curr) == 0:
                        setattr(self, target, curr + "-")
                elif e.unicode.isdigit():
                    curr = getattr(self, target)
                    if len(curr) < 9:
                        setattr(self, target, curr + e.unicode)

            # R pour reset points
            if e.key == pygame.K_r:
                self.start_pt, self.end_pt = None, None

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            # Focus champs
            if self.buffs_rect.collidepoint(mx, my):
                self.focus = "buffs"; return
            if self.bushes_rect.collidepoint(mx, my):
                self.focus = "bushes"; return
            if self.seed_rect.collidepoint(mx, my):
                self.focus = "seed"; return

            # Boutons algo
            if self.grid_btn_rect.collidepoint(mx, my):
                self.algorithm = "grid"; return
            if self.random_btn_rect.collidepoint(mx, my):
                self.algorithm = "random"; return

            # Bouton démarrer
            if self.start_rect.collidepoint(mx, my):
                nb_buffs  = self._parse_int_clamped(self.nb_buffs_str)
                nb_bushes = self._parse_int_clamped(self.nb_bushes_str)
                seed      = self._parse_optional_int(self.seed_str)
                if self.start_pt and self.end_pt and (nb_buffs is not None) and (nb_bushes is not None):
                    from scenes.game import GameScene
                    self.switch_to(
                        GameScene,
                        nb_buffs=nb_buffs,
                        nb_bushes=nb_bushes,
                        start_pt=self.start_pt,
                        end_pt=self.end_pt,
                        placement=self.algorithm,
                        seed=seed,
                    )
                return

            # Sinon : placement / déplacement des points
            if self.start_pt is None:
                self.start_pt = e.pos
            elif self.end_pt is None:
                self.end_pt = e.pos
            else:
                # remplace le plus proche
                sx, sy = self.start_pt
                ex, ey = self.end_pt
                if (mx - sx)**2 + (my - sy)**2 <= (mx - ex)**2 + (my - ey)**2:
                    self.start_pt = e.pos
                else:
                    self.end_pt = e.pos

        elif e.type == pygame.MOUSEBUTTONDOWN and e.button in (2, 3):
            # clic milieu/droit : enlève le focus
            self.focus = None

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill((18, 19, 23))

        # Titre & sous-titre
        title = self.title_font.render("Configurer la partie", True, (240, 240, 255))
        self.screen.blit(title, title.get_rect(center=(self.W//2, 120)))
        sub = self.ui_font.render("Clique pour définir la lane : début puis fin", True, (210, 210, 230))
        self.screen.blit(sub, sub.get_rect(center=(self.W//2, 180)))

        # Preview lane
        if self.start_pt:
            self._draw_point(self.start_pt, (0, 200, 255))
        if self.end_pt:
            self._draw_point(self.end_pt, (255, 140, 0))
        if self.start_pt and self.end_pt:
            pygame.draw.line(self.screen, (120, 200, 255), self.start_pt, self.end_pt, 3)

        # Labels
        buffs_lbl  = self.ui_font.render("Buffs :",  True, (230, 230, 240))
        bushes_lbl = self.ui_font.render("Bushes :", True, (230, 230, 240))
        self.screen.blit(buffs_lbl,  buffs_lbl.get_rect(midleft=self.buffs_label_pos))
        self.screen.blit(bushes_lbl, bushes_lbl.get_rect(midleft=self.bushes_label_pos))

        # Champs texte
        self._draw_input(self.buffs_rect,  self.nb_buffs_str,  "ex: 10",  focused=(self.focus=="buffs"))
        self._draw_input(self.bushes_rect, self.nb_bushes_str, "ex: 30",  focused=(self.focus=="bushes"))

        # Algo + Seed
        mouse = pygame.mouse.get_pos()
        self._draw_label_left((self.W//2 - 220, self.H // 2 + 75), "Algorithme :")
        self._draw_toggle(self.grid_btn_rect,   "GRID",   self.algorithm=="grid",   self.grid_btn_rect.collidepoint(mouse))
        self._draw_toggle(self.random_btn_rect, "RANDOM", self.algorithm=="random", self.random_btn_rect.collidepoint(mouse))

        self._draw_label_left((self.W//2 - 220, self.H // 2 + 75 + 56 + 12), "Seed :")
        self._draw_input(self.seed_rect, self.seed_str, "ex: (vide) ou 42", focused=(self.focus=="seed"))

        # Bouton démarrer
        ready = self.start_pt and self.end_pt and \
                (self._parse_int_clamped(self.nb_buffs_str) is not None) and \
                (self._parse_int_clamped(self.nb_bushes_str) is not None)
        self._draw_button(self.start_rect, "Générer" if ready else "Place les points et saisis des nombres",
                          self.start_rect.collidepoint(pygame.mouse.get_pos()))

        # Aide
        hint = self.small_font.render(
            "Clic: fixer un point • R: reset points • Entrée: valider • Échap: quitter • "
            "Clique dans un champ pour saisir • Choisis l'algo • Seed vide = aléatoire",
            True, (170, 170, 190)
        )
        self.screen.blit(hint, hint.get_rect(center=(self.W//2, self.H - 40)))
