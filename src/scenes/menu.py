import pygame

def run_menu(screen):
    clock = pygame.time.Clock()
    W, H = screen.get_size()
    running = True

    # État
    nb_buffs = 10
    min_buffs, max_buffs = 1, 100

    # Points de lane
    start_pt = None
    end_pt = None

    # Polices
    title_font = pygame.font.SysFont(None, 72)
    ui_font = pygame.font.SysFont(None, 40)
    small_font = pygame.font.SysFont(None, 28)

    # UI rects
    minus_rect = pygame.Rect(W // 2 - 200, H // 2 + 40, 80, 60)
    plus_rect  = pygame.Rect(W // 2 + 120, H // 2 + 40, 80, 60)
    start_rect = pygame.Rect(W // 2 - 160, H // 2 + 140, 320, 64)
    value_rect = pygame.Rect(W // 2 - 100, H // 2 + 40, 200, 60)

    def draw_button(rect, text, hover=False):
        color_bg = (70, 70, 80) if not hover else (100, 100, 120)
        pygame.draw.rect(screen, color_bg, rect, border_radius=12)
        pygame.draw.rect(screen, (150, 150, 170), rect, 2, border_radius=12)
        label = ui_font.render(text, True, (230, 230, 240))
        screen.blit(label, label.get_rect(center=rect.center))

    def draw_point(p, color):
        pygame.draw.circle(screen, color, p, 8)
        pygame.draw.circle(screen, (255, 255, 255), p, 8, 2)

    while running:
        dt = clock.tick(60) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return None
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return None
                if e.key in (pygame.K_RIGHT, pygame.K_KP_PLUS):
                    nb_buffs = min(max_buffs, nb_buffs + 1)
                if e.key in (pygame.K_LEFT, pygame.K_KP_MINUS):
                    nb_buffs = max(min_buffs, nb_buffs - 1)
                if e.key == pygame.K_r:
                    start_pt, end_pt = None, None
                if e.key == pygame.K_RETURN and start_pt and end_pt:
                    return nb_buffs, start_pt, end_pt

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Clic gauche : poser d'abord start, puis end
                if minus_rect.collidepoint(e.pos):
                    nb_buffs = max(min_buffs, nb_buffs - 1)
                elif plus_rect.collidepoint(e.pos):
                    nb_buffs = min(max_buffs, nb_buffs + 1)
                elif start_rect.collidepoint(e.pos):
                    if start_pt and end_pt:
                        return nb_buffs, start_pt, end_pt
                else:
                    if start_pt is None:
                        start_pt = e.pos
                    elif end_pt is None:
                        end_pt = e.pos
                    else:
                        # si les deux existent déjà, on remplace le plus proche
                        sx, sy = start_pt
                        ex, ey = end_pt
                        mx, my = e.pos
                        if (mx - sx)**2 + (my - sy)**2 <= (mx - ex)**2 + (my - ey)**2:
                            start_pt = e.pos
                        else:
                            end_pt = e.pos

        # ---- Rendu ----
        screen.fill((18, 19, 23))

        # Titre
        title = title_font.render("Configurer la partie", True, (240, 240, 255))
        screen.blit(title, title.get_rect(center=(W // 2, 120)))

        # Sous-titre lane
        sub = ui_font.render("Clique pour définir la lane : début puis fin", True, (210, 210, 230))
        screen.blit(sub, sub.get_rect(center=(W // 2, 190)))

        # Zone de prévisualisation (toute la fenêtre ici)
        # Dessiner la ligne si possible
        if start_pt:
            draw_point(start_pt, (0, 200, 255))
        if end_pt:
            draw_point(end_pt, (255, 140, 0))
        if start_pt and end_pt:
            pygame.draw.line(screen, (120, 200, 255), start_pt, end_pt, 3)

        # Contrôles nb buffs
        label_b = ui_font.render("Nombre de buffs :", True, (230, 230, 240))
        screen.blit(label_b, label_b.get_rect(center=(W // 2, H // 2 + 10)))

        draw_button(minus_rect, "–", minus_rect.collidepoint(pygame.mouse.get_pos()))
        draw_button(plus_rect, "+", plus_rect.collidepoint(pygame.mouse.get_pos()))
        pygame.draw.rect(screen, (40, 42, 50), value_rect, border_radius=12)
        pygame.draw.rect(screen, (120, 120, 140), value_rect, 2, border_radius=12)
        label_val = ui_font.render(str(nb_buffs), True, (255, 255, 255))
        screen.blit(label_val, label_val.get_rect(center=value_rect.center))

        # Bouton démarrer
        ready = start_pt and end_pt
        draw_button(start_rect, "Générer" if ready else "Place les 2 points",
                    start_rect.collidepoint(pygame.mouse.get_pos()))

        # Aide
        hint = small_font.render("Clic gauche: fixer un point • R: réinitialiser • Entrée: valider • Échap: quitter",
                                 True, (170, 170, 190))
        screen.blit(hint, hint.get_rect(center=(W // 2, H - 40)))

        pygame.display.flip()
