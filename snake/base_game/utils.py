import pygame


def add_text(game_screen, text, font, size, color, width, height):
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width, height)
    game_screen.blit(text_surface, text_rect)
