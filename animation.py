import pygame
from pygame import Surface
from pathlib import Path
from typing import List, Tuple, Union, Callable


class AnimationSprites:

    def __init__(self):
        self.puff_sprites = None

    def get_puff_sprites(self):
        if self.puff_sprites:
            return self.puff_sprites
        puff = Spritesheet("images/puff_anim_yellow.png", (192, 192))
        sprites = []
        for i in range(7):
            for j in range(5):
                img = pygame.transform.scale(puff.get_sprite((i, j)), (50, 50))
                sprites.append(img)
        self.puff_sprites = sprites
        return self.puff_sprites


class PuffAnimation:

    def __init__(self):
        spritesheet = pygame.image.load("images/puff_anim_yellow.png")
        spritesheet.get_rect()


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


class AnimationsWithCallback:

    def __init__(self,
                 animators: List[Animator],
                 callback: Callable):
        self.animators = animators
        self.callback = callback

    def draw(self, screen: Surface):
        finished = True
        for a in self.animators:
            if a.is_active():
                finished = False
                screen.blit(a.next_frame(), a.coords)
        if finished:
            print("callback")
            self.callback()

    def is_active(self):
        return any([a.is_active() for a in self.animators])


class AnimationProcessor:

    def __init__(self):
        self.animations = []
        self.sprites = AnimationSprites()

    def update(self, screen: Surface):
        self.animations = [a for a in self.animations if a is not None and a.is_active()]
        for a in self.animations:
            a.draw(screen)

    def add_animations(self, animations: List[Animator]):
        self.animations.extend(animations)

    def animate_row_removal(self,
                            row: int,
                            callback: Callable = None):
        print(f"animation {row}")
        animators = []
        for i in range(10):
            animators.append(
                Animator(self.sprites.get_puff_sprites(), (i * 50, row * 50)))
        anims = AnimationsWithCallback(animators, callback)
        self.animations.append(anims)
