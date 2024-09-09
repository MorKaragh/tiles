import logging
from typing import Tuple

import pygame


def get_grid_state_logger():
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('grid_state.log', mode='w')
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def load_img(path: str, size: Tuple[int, int]):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)
