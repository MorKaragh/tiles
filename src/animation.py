from pathlib import Path
from typing import List, Tuple, Union

import pygame
from pygame import Surface


class CyclingAnimation:

    def __init__(self, frames: List, frame_change_rate: int = 1):
        self.frames = frames
        self.frame_counter = 0
        self.change_counter = 0
        self.change_rate = frame_change_rate

    def next_frame(self) -> Surface:
        if self.change_counter == self.change_rate:
            self.change_counter = 0
            self.frame_counter += 1
            if self.frame_counter == len(self.frames):
                self.frame_counter = 0
        else:
            self.change_counter += 1
        return self.frames[self.frame_counter]


class AnimationSprites:

    def __init__(self):
        self.puff_sprites = None

    def get_puff_sprites(self) -> List[Surface]:
        if self.puff_sprites:
            return self.puff_sprites
        puff = Spritesheet("images/puff_anim_yellow.png", (192, 192))
        sprites = []
        for i in range(4, 7):
            for j in range(5):
                img = pygame.transform.scale(puff.get_sprite((i, j)), (50, 50))
                sprites.append(img)
        self.puff_sprites = sprites
        return self.puff_sprites


class Spritesheet:
    def __init__(self,
                 filepath: Path,
                 sprite_size: Tuple[int, int],
                 spacing: Tuple[int, int] = (0, 0),
                 scale: Tuple[int, int] = None) -> None:
        """Initialize the spritesheet.

        Args:
            filepath (Path): Path to the spritesheet image file.
            sprite_size (Tuple[int, int]): Width and height of each sprite in the sheet.
            spacing (Tuple[int, int], optional): Spacing between each sprite (row spacing, column spacing). Defaults to (0, 0).
            scale (Tuple[int, int], optional): Rescale each sprite to the given size. Defaults to None.
        """
        self._sheet = pygame.image.load(filepath).convert_alpha()
        self._sprite_size = sprite_size
        self._spacing = spacing
        self._scale = scale

    def get_sprite(self,
                   loc: Tuple[int, int],
                   colorkey: Union[pygame.Color, int, None] = None) -> pygame.Surface:
        """Load a specific sprite from the spritesheet.

        Args:
            loc (Tuple[int, int]): Location of the sprite in the sheet (row, column).
            colorkey (Union[pygame.Color, int, None], optional): Color to be treated as transparent. Defaults to None.

        Returns:
            pygame.Surface: The sprite image.
        """
        x = loc[1] * (self._sprite_size[0] + self._spacing[0])
        y = loc[0] * (self._sprite_size[1] + self._spacing[1])

        rect = pygame.Rect(x, y, *self._sprite_size)
        image = pygame.Surface(
            self._sprite_size, pygame.SRCALPHA).convert_alpha()
        image.blit(self._sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        if self._scale:
            image = pygame.transform.scale(image, self._scale)

        return image

    def get_sprites(self,
                    locs: List[Tuple[int, int]],
                    colorkey: Union[pygame.Color, int, None] = None) -> List[pygame.Surface]:
        """Load multiple sprites from the spritesheet.

        Args:
            locs (List[Tuple[int, int]]): List of locations of the sprites in the sheet (row, column).
            colorkey (Union[pygame.Color, int, None], optional): Color to be treated as transparent. Defaults to None.

        Returns:
            List[pygame.Surface]: List of sprite images.
        """
        return [self.get_sprite(loc, colorkey) for loc in locs]


class Animator:

    def __init__(self,
                 sprites: List[Surface],
                 coords: Tuple[int, int],
                 delay: int = 0):
        self.delay = delay
        self.pointer = 0
        self.sprites = sprites
        self.coords = coords

    def next_frame(self):
        if self.delay < 0:
            self.delay += 1
        else:
            if self.is_active():
                to_return = self.sprites[self.pointer]
                self.pointer += 1
                return to_return

    def is_active(self):
        return self.pointer < len(self.sprites)


class AnimatorFactory:

    def __init__(self):
        self.sprites = AnimationSprites()

    def get_square_puff(self, coords: Tuple[int, int], delay: int = 0):
        return Animator(self.sprites.get_puff_sprites(), coords, delay)

    def get_gold_frame_amin(self, width: int):
        return CyclingAnimation(self.sprites.get_gold_frame_sprites(width), 5)
