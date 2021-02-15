import Shared.constants.GameConstants as GameConstants;

import pygame;
import sys;


def GetMousePosition():
    mouseX, mouseY = pygame.mouse.get_pos();

    return (mouseX, mouseY);


def Label(screen, text, x, y):
    font = pygame.font.SysFont(None, 20);
    label = font.render(text, 1, (0,0,0));
    labelRect = label.get_rect();
    labelRect.topleft = (x, y);
    screen.blit(label, labelRect);

    return labelRect;

def Button(screen, text, x, y):
    font = pygame.font.SysFont(None, 20);
    button = font.render(text, 1, (0,0,0));
    buttonRect = button.get_rect();
    buttonRect.topleft = (x, y);
    screen.blit(button, buttonRect);

    return buttonRect;