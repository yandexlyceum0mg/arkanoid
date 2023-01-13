from __future__ import annotations
import os
import random
import time

from pygame import display
import pygame

TEST = False

random.seed(0)


class Line(pygame.sprite.Sprite):
    def __init__(self, a, b, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((a, b), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, a, b), a)
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y


class T(pygame.sprite.Sprite):
    def __init__(self, a, b, x, y, g):
        super().__init__(g)
        self.image = pygame.Surface((a, b), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, a, b), a)
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y


class Block(pygame.sprite.Sprite):
    def __init__(self, board, a, b, x, y, group, col, breaking=1):
        class HLine1(pygame.sprite.Sprite):
            def __init__(self, block, group):
                super().__init__(group)
                self.image = pygame.Surface((block.a, 1), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, (0, 0, 0), (0, 0, block.a, 1), 1)
                self.rect = self.image.get_rect().move(block.x, block.y)
                self.x = self.rect.x
                self.y = self.rect.y

        class HLine2(pygame.sprite.Sprite):
            def __init__(self, block, group):
                super().__init__(group)
                self.image = pygame.Surface((block.a, 1), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, (0, 0, 0), (0, 0, block.a, 1), 1)
                self.rect = self.image.get_rect().move(block.x, block.y + block.rect.height - 1)
                self.x = self.rect.x
                self.y = self.rect.y

        class VLine1(pygame.sprite.Sprite):
            def __init__(self, block, group):
                super().__init__(group)
                self.image = pygame.Surface((1, block.b), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 1, block.b), 1)
                self.rect = self.image.get_rect().move(block.x, block.y)
                self.x = self.rect.x
                self.y = self.rect.y

        class VLine2(pygame.sprite.Sprite):
            def __init__(self, block, group):
                super().__init__(group)
                self.image = pygame.Surface((1, block.b), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 1, block.b), 1)
                self.rect = self.image.get_rect().move(block.x + block.rect.width - 1, block.y)
                self.x = self.rect.x
                self.y = self.rect.y

        self.board = board
        self.xy = (x, y)
        if board.lvl < 10:
            self.char = random.choice(list('LEPMT') + [None] * 30)
        elif board.lvl < 20:
            self.char = random.choice(list('LESPMT') + [None] * 30)
        else:
            self.char = random.choice(Capsule.chars + [None] * 30)
        self.br = breaking

        def f(x, y):
            a = int(x[0] * y)
            if a > 255:
                a = 255
            b = int(x[1] * y)
            if b > 255:
                b = 255
            c = int(x[2] * y)
            if c > 255:
                c = 255
            return tuple([a, b, c])

        self.f = f
        self.col = col
        self.a = a
        self.b = b
        super().__init__(*group)
        self.image = pygame.Surface((a, b), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, col, (0, 0, a, b), a)
        self.rect = self.image.get_rect()
        self.breaking = breaking
        if self.breaking == 1:
            coef = 0.65
            pygame.draw.rect(self.image, f(col, coef), (a // 16, b // 8 * 6, a // 16 * 14, b // 8))
            pygame.draw.rect(self.image, f(col, coef), (a // 16 * 2, b // 8 * 5, a // 16 * 13, b // 8))
            pygame.draw.rect(self.image, f(col, coef), (a // 16 * 13, b // 8, a // 16, b // 8 * 6))
            pygame.draw.rect(self.image, f(col, coef), (a // 16 * 14, 0, a // 16, b // 16 * 15))
        else:
            coef1 = 0.75
            coef2 = 0.5
            pygame.draw.rect(self.image, f(col, coef1), (a // 16, b // 8 * 6, a // 16 * 14, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 2, b // 8 * 5, a // 16 * 13, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 3, b // 8 * 4, a // 16 * 12, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 3, b // 8 * 2, a // 16 * 12, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 2, b // 8, a // 16 * 13, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16, 0, a // 16 * 14, b // 8))

            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 11, b // 8 * 3, a // 16, b // 8))
            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 12, b // 8 * 2, a // 16, b // 8 * 3))
            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 13, b // 8, a // 16, b // 8 * 5))
            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 14, 0, a // 16, b // 8 * 7))

        pygame.draw.rect(self.image, (0, 0, 0), (0, b // 8 * 7, a, b // 8))
        pygame.draw.rect(self.image, (0, 0, 0), (a // 16 * 15, 0, a // 16, b))

        self.x = x
        self.y = y
        self.g = group
        self.coef = 0.65
        self.coef1 = 0.75
        self.coef2 = 0.5
        self.coef0 = 1
        self.iscolide = 0
        self.isnotadded = True
        self.vl1 = VLine1(self, board._lines)
        self.vl2 = VLine2(self, board._lines)
        self.hl1 = HLine1(self, board._lines)
        self.hl2 = HLine2(self, board._lines)

    def collide__(self):
        if self.br == 0:
            return None
        self.br -= 1
        if self.br == 0:
            self.kill()
            self.board.upscore(40)
            Capsule(Capsule.cols[self.char], self.a, self.b, self.rect.x, self.rect.y, self.char, self.board.cs)
        else:
            self.iscolide = 1

    def _ball(self, ball: Ball):
        if ball.flag:
            return
        if pygame.sprite.collide_mask(ball, self.vl1):
            ball.vx = - abs(ball.vy) + (128 - int(os.urandom(1).hex(), 16)) // 16
            self.board.upscore(10)
        if pygame.sprite.collide_mask(ball, self.vl2):
            ball.vx = abs(ball.vy) + (128 - int(os.urandom(1).hex(), 16)) // 16
            self.board.upscore(10)
        if pygame.sprite.collide_mask(ball, self.hl1):
            ball.vy = - abs(ball.vy) + (128 - int(os.urandom(1).hex(), 16)) // 16
            self.board.upscore(10)
        if pygame.sprite.collide_mask(ball, self.hl2):
            ball.vy = abs(ball.vy) + (128 - int(os.urandom(1).hex(), 16)) // 16
            self.board.upscore(10)

    def update(self):
        if self.iscolide == 1 and (self.f(self.col, self.coef)[0] != 255 and self.f(self.col, self.coef)[1] != 255 and
                                   self.f(self.col, self.coef)[2] != 255):
            self.coef += 0.01
            self.coef0 += 0.01
            self.coef1 += 0.01
            self.coef2 += 0.01
        elif self.iscolide != 0:
            self.ud = False
            self.iscolide = -1
            if self.iscolide == -1 and self.coef2 > 0.5:
                self.coef -= 0.01
                self.coef0 -= 0.01
                self.coef1 -= 0.01
                self.coef2 -= 0.01
            else:
                self.ud = True
                self.iscolide = 0
        f = self.f
        col = self.col
        a = self.a
        b = self.b
        coef0 = self.coef0
        pygame.draw.rect(self.image, f(col, coef0), (0, 0, a, b), a)
        if self.breaking == 1:
            coef = self.coef
            pygame.draw.rect(self.image, f(col, coef), (a // 16, b // 8 * 6, a // 16 * 14, b // 8))
            pygame.draw.rect(self.image, f(col, coef), (a // 16 * 2, b // 8 * 5, a // 16 * 13, b // 8))
            pygame.draw.rect(self.image, f(col, coef), (a // 16 * 13, b // 8, a // 16, b // 8 * 6))
            pygame.draw.rect(self.image, f(col, coef), (a // 16 * 14, 0, a // 16, b // 16 * 15))
        else:
            coef1 = self.coef1
            coef2 = self.coef2
            pygame.draw.rect(self.image, f(col, coef1), (a // 16, b // 8 * 6, a // 16 * 14, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 2, b // 8 * 5, a // 16 * 13, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 3, b // 8 * 4, a // 16 * 12, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 3, b // 8 * 2, a // 16 * 12, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16 * 2, b // 8, a // 16 * 13, b // 8))
            pygame.draw.rect(self.image, f(col, coef1), (a // 16, 0, a // 16 * 14, b // 8))

            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 11, b // 8 * 3, a // 16, b // 8))
            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 12, b // 8 * 2, a // 16, b // 8 * 3))
            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 13, b // 8, a // 16, b // 8 * 5))
            pygame.draw.rect(self.image, f(col, coef2), (a // 16 * 14, 0, a // 16, b // 8 * 7))

        pygame.draw.rect(self.image, (0, 0, 0), (0, b // 8 * 7, a, b // 8))
        pygame.draw.rect(self.image, (0, 0, 0), (a // 16 * 15, 0, a // 16, b))
        self.rect = self.rect.move((self.x, self.y))
        self.rect.x = self.x
        self.rect.y = self.y
        if self.isnotadded:
            self.g.add(self)
            self.isnotadded = False


class Capsule(pygame.sprite.Sprite):
    chars = list('LESBPMTN')
    cols = {'L': (255 // 2, 255, 0), 'E': (0, 0, 255), 'S': (255, 0, 255), 'B': (255, 0, 0), 'P': (0, 0, 0),
            'M': (0, 255, 255), 'T': (0, 255, 255), 'N': (150, 150, 255), None: None}

    def __init__(self, col, a, b, x, y, char, group):
        super().__init__(group)

        def f(x, y):
            a = int(x[0] + y)
            if a > 255:
                a = 255
            b = int(x[1] + y)
            if b > 255:
                b = 255
            c = int(x[2] + y)
            if c > 255:
                c = 255
            return tuple([a, b, c])

        if char is None:
            self.kill()
            return
        w = (255, 255, 255)
        c = 100
        self.image = pygame.Surface((a, b // 8 * 7), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, f(col, c), (0, b // 8, a // 16, b // 8 * 5), a)
        pygame.draw.rect(self.image, f(col, c), (a // 16, 0, a // 16 * 14, b // 8 * 7), a)
        pygame.draw.rect(self.image, f(col, c), (a // 16 * 15, b // 8, a // 16, b // 8 * 5), a)
        pygame.draw.rect(self.image, w, (0, b // 8 * 2, a // 16, b // 8), a)
        pygame.draw.rect(self.image, w, (a // 16, b // 8, a // 16 * 13, b // 8), a)
        pygame.draw.rect(self.image, col, (a // 16, b // 8 * 3, a // 16, b // 8 * 2), a)
        pygame.draw.rect(self.image, col, (a // 16 * 2, b // 8 * 2, a // 16 * 12, b // 8 * 4), a)
        pygame.draw.rect(self.image, col, (a // 16 * 14, b // 8 * 3, a // 16, b // 8 * 2), a)

        font = pygame.font.Font(None, b // 8 * 10)
        txt = font.render(char, True, (255, 255, 0))
        self.rect = txt.get_rect().move(x, y)
        self.image.blit(txt, (a // 16 * 6, b // 8))
        self.vy = 1
        self.char = char

    def update(self):
        self.rect.y += self.vy

    def ____(self, board):
        if self.char == 'L':
            board.pl.func = board.pl.laser
            board.ball.standart()
        if self.char == 'E':
            if board.pl.func == board.pl.wide or board.pl.func == board.pl.ultrawide:
                board.pl.func = board.pl.ultrawide
            else:
                board.pl.func = board.pl.wide
            board.ball.standart()
        if self.char == 'S':
            board.pl.func = board.pl.standart
            board.ball.standart()
        if self.char == 'B':
            board.pl.func = board.pl.standart
            board.c -= 1
            if board.c < 0:
                board.go = True
            board.ball.standart()
        if self.char == 'P':
            board.pl.func = board.pl.standart
            board.c += 1
            board.ball.standart()
        if self.char == 'M':
            board.pl.func = board.pl.standart
            board.ball.m()
        if self.char == 'T':
            board.pl.func = board.pl.standart
            T(board.cell_size1 * board.width, 1, board.left, board.pl.rect.y + board.pl.a // 16 * 4, board.gt)
            board.ball.standart()
        if self.char == 'N':
            board.lvl += 1
            random.seed(board.lvl)
            board.set_view(board.left, board.top, board.cell_size1, board.cell_size2)
            board.upscore(2000)
            board.ball.standart()


class FlyingOpponent(pygame.sprite.Sprite):
    def __init__(self, board):
        super().__init__(board.f)
        a = board.cell_size1
        b = board.cell_size2
        col = tuple([random.randint(0, 255) for _ in range(3)])

        def f(x, y):
            a = int(x[0] * y)
            if a > 255:
                a = 255
            b = int(x[1] * y)
            if b > 255:
                b = 255
            c = int(x[2] * y)
            if c > 255:
                c = 255
            return tuple([a, b, c])

        self.image = pygame.Surface((a // 16 * 15, b // 8 * 7), pygame.SRCALPHA, 32)
        coef = 0.65
        pygame.draw.rect(self.image, col, (0, 0, a // 16 * 15, b // 8 * 7), a)
        pygame.draw.rect(self.image, f(col, coef), (a // 16, b // 8 * 6, a // 16 * 14, b // 8))
        pygame.draw.rect(self.image, f(col, coef), (a // 16 * 2, b // 8 * 5, a // 16 * 13, b // 8))
        pygame.draw.rect(self.image, f(col, coef), (a // 16 * 13, b // 8, a // 16, b // 8 * 6))
        pygame.draw.rect(self.image, f(col, coef), (a // 16 * 14, 0, a // 16, b // 16 * 15))
        self.rect = self.image.get_rect().move(random.randint(board.left, board.left + board.width * board.cell_size1),
                                               random.randint(board.top, board.top + board.height * board.cell_size2))
        self.vx = random.choice([random.randint(1, 100), random.randint(-100, -1)])
        self.vy = random.choice([random.randint(1, 100), random.randint(-100, -1)])
        self._x = self.rect.x * 1000
        self._y = self.rect.y * 1000

    def update(self):
        self._x += self.vx * 3
        self._y += self.vy * 3
        self.rect.x = self._x // 1000
        self.rect.y = self._y // 1000


class Fon(pygame.sprite.Sprite):
    def __init__(self, a, x, y, group):
        super().__init__(group)
        self.col = (0, 0, 200)

        def f(x, y):
            a = int(x[0] * y)
            if a > 255:
                a = 255
            b = int(x[1] * y)
            if b > 255:
                b = 255
            c = int(x[2] * y)
            if c > 255:
                c = 255
            return tuple([a, b, c])

        self.a = a
        self.f = f
        self.x = x
        self.y = y
        self.image = pygame.Surface((a, a), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, self.col, (0, 0, a, a), a)
        self.rect = self.image.get_rect()
        self.coef1 = 0.8
        self.coef2 = 0.6
        for i in range(12):
            pygame.draw.rect(self.image, f(self.col, self.coef2), (0, a // 16 * i, a // 16 * (12 - i), a // 16),
                             a // 16)

        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 12, 0, a // 16 * 4, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 11, a // 16 * 1, a // 16 * 5, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 10, a // 16 * 2, a // 16 * 6, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 9, a // 16 * 3, a // 16 * 7, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 8, a // 16 * 4, a // 16 * 8, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 8, a // 16 * 5, a // 16 * 8, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 8, a // 16 * 6, a // 16 * 8, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 8, a // 16 * 7, a // 16 * 8, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 12, a // 16 * 8, a // 16 * 4, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 13, a // 16 * 9, a // 16 * 3, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 14, a // 16 * 10, a // 16 * 2, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 15, a // 16 * 11, a // 16 * 1, a // 16))

        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 4, a // 16 * 8, a // 16 * 4, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 3, a // 16 * 9, a // 16 * 5, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16 * 2, a // 16 * 10, a // 16 * 6, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (a // 16, a // 16 * 11, a // 16 * 7, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (0, a // 16 * 12, a // 16 * 9, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (0, a // 16 * 13, a // 16 * 10, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (0, a // 16 * 14, a // 16 * 11, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef1), (0, a // 16 * 15, a // 16 * 12, a // 16))

        pygame.draw.rect(self.image, f(self.col, self.coef2), (a // 16 * 8, a // 16 * 8, a // 16 * 3, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef2), (a // 16 * 8, a // 16 * 9, a // 16 * 2, a // 16))
        pygame.draw.rect(self.image, f(self.col, self.coef2), (a // 16 * 8, a // 16 * 10, a // 16, a // 16))

        self.rect.x = self.x
        self.rect.y = self.y


class L(pygame.sprite.Sprite):
    def __init__(self, a, x, y, group):
        super().__init__(group)
        self.image = pygame.Surface((a // 16 * 2, a // 16 * 8), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, a // 16 * 2, a // 16 * 8), a // 16 * 2)
        self.rect = self.image.get_rect().move(x, y)
        self.vy = -8

    def update(self):
        self.rect.y += self.vy

    def __colide(self):
        self.kill()


class Platform(pygame.sprite.Sprite):
    def __init__(self, board, a, x, y, group):
        super().__init__(group)
        self.board = board

        def f(x, y):
            a = int(x[0] * y)
            if a > 255:
                a = 255
            b = int(x[1] * y)
            if b > 255:
                b = 255
            c = int(x[2] * y)
            if c > 255:
                c = 255
            return tuple([a, b, c])

        self.f = f
        self.a = a
        w = (255, 255, 255)
        r1 = (200, 0, 0)
        r2 = (255, 80, 80)
        r3 = (150, 0, 0)
        r4 = (100, 0, 0)
        b = (0, 0, 0)
        g1 = (150, 150, 150)
        g2 = (210, 210, 210)
        g3 = (110, 110, 110)
        g4 = (50, 50, 50)
        g5 = (80, 80, 80)
        g6 = (130, 130, 130)
        self.b = (0, 0, 255)
        self.image = pygame.Surface((a * 2, a // 2), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, w, (0, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 31, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 3, 0, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 3, a // 16, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 3, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 1, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 3, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 2, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 6, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 3, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 6, 0, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 7, a // 16, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, 0, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 8, a // 16 * 2, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16 * 3, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, a // 16 * 4, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 8, a // 16 * 5, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 8, a // 16 * 6, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 14, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 10, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 14, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 17, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 21, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 10, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 10, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 21, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 21, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 10, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 10, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 21, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 21, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 24, a // 16, a // 16, a // 16 * 6), a // 16)

        pygame.draw.rect(self.image, r4, (a // 16 * 25, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 25, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 29, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 25, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 25, a // 16 * 1, a // 16 * 4, a // 16 * 3), a // 16 * 2)
        pygame.draw.rect(self.image, w, (a // 16 * 25, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 25, 0, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 29, a // 16 * 1, a // 16, a // 16 * 5), a // 16)
        self._x = x
        self._y = y
        self.x = self._x - a
        self.y = self._y
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.ud = True
        self.coef1 = 0.2
        self.coef2 = 0.5
        self.f1()
        self.flag = 2
        self.islaser = False
        self.func = self.standart

    def set_field_and_size(self, f, s):
        self.field = f
        self.size = s

    def standart(self, x):
        a = self.a
        w = (255, 255, 255)
        r1 = (200, 0, 0)
        r2 = (255, 80, 80)
        r3 = (150, 0, 0)
        r4 = (100, 0, 0)
        b = (0, 0, 0)
        g1 = (150, 150, 150)
        g2 = (210, 210, 210)
        g3 = (110, 110, 110)
        g4 = (50, 50, 50)
        g5 = (80, 80, 80)
        g6 = (130, 130, 130)
        self.b = (0, 0, 255)
        self.image = pygame.Surface((a * 2, a // 2), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, w, (0, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 31, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 3, 0, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 3, a // 16, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 3, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 1, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 3, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 2, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 6, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 3, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 6, 0, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 7, a // 16, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, 0, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 8, a // 16 * 2, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16 * 3, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, a // 16 * 4, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 8, a // 16 * 5, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 8, a // 16 * 6, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 14, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 10, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 14, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 17, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 21, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 10, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 10, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 21, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 21, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 10, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 10, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 21, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 21, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 24, a // 16, a // 16, a // 16 * 6), a // 16)

        pygame.draw.rect(self.image, r4, (a // 16 * 25, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 25, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 29, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 25, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 25, a // 16 * 1, a // 16 * 4, a // 16 * 3), a // 16 * 2)
        pygame.draw.rect(self.image, w, (a // 16 * 25, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 25, 0, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 29, a // 16 * 1, a // 16, a // 16 * 5), a // 16)
        self._x = x
        self.x = self._x - a
        self.rect.x = self.x
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
        self.f1()
        self.flag = 2
        self.islaser = False

    def wide(self, x):
        a = self.a
        w = (255, 255, 255)
        r1 = (200, 0, 0)
        r2 = (255, 80, 80)
        r3 = (150, 0, 0)
        r4 = (100, 0, 0)
        b = (0, 0, 0)
        g1 = (150, 150, 150)
        g2 = (210, 210, 210)
        g3 = (110, 110, 110)
        g4 = (50, 50, 50)
        g5 = (80, 80, 80)
        g6 = (130, 130, 130)
        self.b = (0, 0, 255)
        self.image = pygame.Surface((a * 3, a // 2), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, w, (0, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 47, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 3, 0, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 3, a // 16, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 3, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 1, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 3, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 2, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 6, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 3, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 6, 0, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 7, a // 16, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, 0, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 8, a // 16 * 2, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16 * 3, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, a // 16 * 4, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 8, a // 16 * 5, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 8, a // 16 * 6, a // 16 * 32, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 8, a // 16 * 4, a // 16 * 2, a // 16 * 2), a // 16 * 2)
        pygame.draw.rect(self.image, g4, (a // 16 * 9, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 22, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 13, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 13, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 13, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 13, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 13, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 18, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 18, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 18, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 18, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 18, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 22, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 25, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 29, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 29, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 29, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 29, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 29, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 34, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 34, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 34, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 34, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 34, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 38, a // 16 * 4, a // 16 * 2, a // 16 * 2), a // 16 * 2)
        pygame.draw.rect(self.image, g4, (a // 16 * 38, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 40, a // 16, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 41, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 41, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 45, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 41, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 41, a // 16 * 1, a // 16 * 4, a // 16 * 3), a // 16 * 2)
        pygame.draw.rect(self.image, w, (a // 16 * 41, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 41, 0, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 45, a // 16 * 1, a // 16, a // 16 * 5), a // 16)
        self._x = x
        self.x = self._x - int(a * 1.5)
        self.rect.x = self.x
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
        self.f2()
        self.flag = 3
        self.islaser = False

    def ultrawide(self, x):
        a = self.a
        w = (255, 255, 255)
        r1 = (200, 0, 0)
        r2 = (255, 80, 80)
        r3 = (150, 0, 0)
        r4 = (100, 0, 0)
        b = (0, 0, 0)
        g1 = (150, 150, 150)
        g2 = (210, 210, 210)
        g3 = (110, 110, 110)
        g4 = (50, 50, 50)
        g5 = (80, 80, 80)
        g6 = (130, 130, 130)
        self.b = (0, 0, 255)
        self.image = pygame.Surface((a * 4, a // 2), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, w, (0, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 63, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 3, 0, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 3, a // 16, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 3, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 1, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 2, a // 16 * 3, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 2, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 2, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 6, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 3, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 6, 0, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 7, a // 16, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, 0, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 8, a // 16 * 2, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16 * 3, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, a // 16 * 4, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 8, a // 16 * 5, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 8, a // 16 * 6, a // 16 * 48, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 10, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 10, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 10, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 10, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 10, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 14, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 14, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 17, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 21, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 21, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 21, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 21, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 21, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 26, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 26, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 26, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 26, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 26, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 30, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 30, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 33, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 37, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 37, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 37, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 37, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 37, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 42, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 42, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 42, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 42, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 42, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 46, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 46, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 49, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 53, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 53, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 53, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 53, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 53, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 56, a // 16, a // 16, a // 16 * 6), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 57, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 57, a // 16 * 6, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r4, (a // 16 * 61, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 57, a // 16 * 4, a // 16 * 4, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, r2, (a // 16 * 57, a // 16 * 1, a // 16 * 4, a // 16 * 3), a // 16 * 2)
        pygame.draw.rect(self.image, w, (a // 16 * 57, a // 16 * 2, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, r1, (a // 16 * 57, 0, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, r3, (a // 16 * 61, a // 16 * 1, a // 16, a // 16 * 5), a // 16)
        self._x = x
        self.x = self._x - a * 2
        self.rect.x = self.x
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
        self.f3()
        self.flag = 4
        self.islaser = False

    def laser(self, x):
        a = self.a
        w = (255, 255, 255)
        b = (0, 0, 0)
        g1 = (80, 80, 80)
        g2 = (100, 100, 100)
        g3 = (130, 130, 130)
        g4 = (160, 160, 160)
        g5 = (210, 210, 210)
        g6 = (220, 220, 220)
        blue = (0, 0, 150)
        y1 = (200, 200, 0)
        y2 = (255, 255, 150)
        self.image = pygame.Surface((a * 2, a // 2), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, g4, (a // 16 * 3, 0, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 2, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 3, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 4, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 5, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 6, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 2, a // 16 * 2, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 4, a // 16 * 2, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 6, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (0, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16, a // 16 * 3, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 4, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, blue, (a // 16 * 5, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 6, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (0, a // 16 * 4, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, blue, (a // 16 * 4, a // 16 * 4, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 6, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (0, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16, a // 16 * 5, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 4, a // 16 * 5, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 6, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16, a // 16 * 6, a // 16 * 6, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 4, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 2, a // 16 * 7, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 3, a // 16 * 7, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 7, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 7, a // 16 * 2, a // 16, a // 16 * 2), a // 16)

        pygame.draw.rect(self.image, w, (a // 16 * 8, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 8, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 8, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 8, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 8, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 8, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 8, a // 16 * 7, a // 16 * 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 9, 0, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 9, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 9, a // 16 * 3, a // 16, a // 16 * 4), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 10, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 10, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 10, a // 16 * 3, a // 16, a // 16 * 4), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 11, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 11, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 11, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 11, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 11, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 12, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 12, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 12, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 12, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 12, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 12, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 12, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 13, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 13, a // 16, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 13, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 13, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 13, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 13, a // 16 * 6, a // 16 * 6, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 14, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 14, a // 16 * 2, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 14, a // 16 * 3, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 14, a // 16 * 4, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 14, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, y2, (a // 16 * 15, 0, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 15, a // 16, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 15, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 16, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 16, a // 16 * 4, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 16, a // 16 * 5, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 17, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 17, a // 16, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 18, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 18, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 18, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 18, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 19, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 19, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 19, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 19, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 19, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 19, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 19, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 20, a // 16, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 20, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 20, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 20, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 20, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, y1, (a // 16 * 21, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 21, a // 16 * 3, a // 16, a // 16 * 4), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 22, 0, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 22, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 22, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 22, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 22, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g6, (a // 16 * 22, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 23, 0, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 23, a // 16 * 2, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 23, a // 16 * 3, a // 16, a // 16 * 4), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 24, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 24, a // 16 * 3, a // 16, a // 16), a // 16)

        pygame.draw.rect(self.image, g4, (a // 16 * 25, 0, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 25, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 26, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g1, (a // 16 * 27, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 28, a // 16, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 29, a // 16, a // 16, a // 16), a // 16)

        pygame.draw.rect(self.image, w, (a // 16 * 25, a // 16 * 2, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 26, a // 16 * 2, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 28, a // 16 * 2, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 30, a // 16 * 2, a // 16, a // 16), a // 16)

        pygame.draw.rect(self.image, g5, (a // 16 * 25, a // 16 * 3, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, w, (a // 16 * 26, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, blue, (a // 16 * 27, a // 16 * 3, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g5, (a // 16 * 28, a // 16 * 3, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 31, a // 16 * 3, a // 16, a // 16 * 2), a // 16)

        pygame.draw.rect(self.image, blue, (a // 16 * 26, a // 16 * 4, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 28, a // 16 * 4, a // 16 * 4, a // 16), a // 16)

        pygame.draw.rect(self.image, g4, (a // 16 * 25, a // 16 * 5, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 26, a // 16 * 5, a // 16 * 2, a // 16), a // 16)
        pygame.draw.rect(self.image, g4, (a // 16 * 28, a // 16 * 5, a // 16 * 3, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 31, a // 16 * 5, a // 16, a // 16), a // 16)

        pygame.draw.rect(self.image, g3, (a // 16 * 25, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 26, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 27, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g2, (a // 16 * 28, a // 16 * 6, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, g3, (a // 16 * 29, a // 16 * 6, a // 16 * 2, a // 16), a // 16)

        pygame.draw.rect(self.image, g3, (a // 16 * 26, a // 16 * 7, a // 16 * 4, a // 16), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 7, a // 16 * 4, a // 16, a // 16 * 3), a // 16)
        pygame.draw.rect(self.image, b, (a // 16 * 24, a // 16 * 4, a // 16, a // 16 * 3), a // 16)

        self._x = x
        self.x = self._x - a
        self.rect.x = self.x
        self.flag = 2
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)
        self.islaser = True

    def update(self, x):
        self.func(x)
        if 'field' in self.__dict__:
            if self.rect.x < self.field:
                self.rect.x = self.field
            elif self.rect.x > self.field + self.size - self.rect.width:
                self.rect.x = self.field + self.size - self.rect.width

    def f1(self):
        a = self.a
        f = self.f
        if self.ud:
            if self.coef1 < 1:
                self.coef1 += 0.005
            if self.coef2 < 1:
                self.coef2 += 0.01
            else:
                self.ud = False
        if not self.ud:
            if self.coef1 > 0.2:
                self.coef1 -= 0.005
            if self.coef2 > 0.2:
                self.coef2 -= 0.01
            else:
                self.ud = True
        pygame.draw.rect(self.image, f(self.b, self.coef1), (0, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef2), (a // 16, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16 * 31, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16 * 30, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef2), (a // 16 * 30, a // 16 * 4, a // 16, a // 16 * 2), a // 16)

    def f2(self):
        a = self.a
        f = self.f
        if self.ud:
            if self.coef1 < 1:
                self.coef1 += 0.005
            if self.coef2 < 1:
                self.coef2 += 0.01
            else:
                self.ud = False
        if not self.ud:
            if self.coef1 > 0.2:
                self.coef1 -= 0.005
            if self.coef2 > 0.2:
                self.coef2 -= 0.01
            else:
                self.ud = True
        pygame.draw.rect(self.image, f(self.b, self.coef1), (0, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef2), (a // 16, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16 * 47, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16 * 46, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef2), (a // 16 * 46, a // 16 * 4, a // 16, a // 16 * 2), a // 16)

    def f3(self):
        a = self.a
        f = self.f
        if self.ud:
            if self.coef1 < 1:
                self.coef1 += 0.005
            if self.coef2 < 1:
                self.coef2 += 0.01
            else:
                self.ud = False
        if not self.ud:
            if self.coef1 > 0.2:
                self.coef1 -= 0.005
            if self.coef2 > 0.2:
                self.coef2 -= 0.01
            else:
                self.ud = True
        pygame.draw.rect(self.image, f(self.b, self.coef1), (0, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef2), (a // 16, a // 16 * 4, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16 * 63, a // 16 * 4, a // 16, a // 16), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef1), (a // 16 * 62, a // 16 * 2, a // 16, a // 16 * 2), a // 16)
        pygame.draw.rect(self.image, f(self.b, self.coef2), (a // 16 * 62, a // 16 * 4, a // 16, a // 16 * 2), a // 16)

    def l(self):
        if self.islaser:
            L(self.a, self.rect.x + self.a // 16 * 11, self.y + self.a // 16, self.board.ls)
            L(self.a, self.rect.x + self.a // 16 * 21, self.y + self.a // 16, self.board.ls)


class Ball(pygame.sprite.Sprite):
    def __init__(self, a, x, y, platform: Platform, group):
        super().__init__(group)
        self.flag = False
        self.pl = platform
        self.y = y
        self.x = x
        self.image = pygame.Surface((a, a), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255), (0, a // 5, a // 5, a // 5 * 3))
        pygame.draw.rect(self.image, (255, 255, 255), (a // 5 * 4, a // 5, a // 5, a // 5 * 3), a // 5)
        self.ball = pygame.draw.rect(self.image, (255, 255, 255), (a // 5, 0, a // 5 * 3, a // 5), a // 5)
        self.ball = pygame.draw.rect(self.image, (255, 255, 255), (a // 5, a // 5 * 4, a // 5 * 3, a // 5), a // 5)
        pygame.draw.rect(self.image, (0, 0, 255), (a // 5, a // 5, a // 5 * 3, a // 5 * 3), a // 5 * 3)
        self.rect = self.image.get_rect().move(x, y)
        self.vx = 0
        self.vy = 0
        self.c = [x * 1000, y * 1000]
        self.flight = False
        self.a = a

    def standart(self):
        a = self.a
        self.flag = False
        self.image = pygame.Surface((a, a), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255), (0, a // 5, a // 5, a // 5 * 3))
        pygame.draw.rect(self.image, (255, 255, 255), (a // 5 * 4, a // 5, a // 5, a // 5 * 3), a // 5)
        self.ball = pygame.draw.rect(self.image, (255, 255, 255), (a // 5, 0, a // 5 * 3, a // 5), a // 5)
        self.ball = pygame.draw.rect(self.image, (255, 255, 255), (a // 5, a // 5 * 4, a // 5 * 3, a // 5), a // 5)
        pygame.draw.rect(self.image, (0, 0, 255), (a // 5, a // 5, a // 5 * 3, a // 5 * 3), a // 5 * 3)
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)

    def m(self):
        a = self.a
        self.flag = True
        self.image = pygame.Surface((a, a), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (255, 255, 255), (0, a // 5, a // 5, a // 5 * 3))
        pygame.draw.rect(self.image, (255, 255, 255), (a // 5 * 4, a // 5, a // 5, a // 5 * 3), a // 5)
        self.ball = pygame.draw.rect(self.image, (255, 255, 255), (a // 5, 0, a // 5 * 3, a // 5), a // 5)
        self.ball = pygame.draw.rect(self.image, (255, 255, 255), (a // 5, a // 5 * 4, a // 5 * 3, a // 5), a // 5)
        pygame.draw.rect(self.image, (0, 255, 0), (a // 5, a // 5, a // 5 * 3, a // 5 * 3), a // 5 * 3)
        self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)

    def platformhit(self):
        if self.pl.rect.x + self.pl.a // 2 > self.rect.center[0]:
            self.enter(3, -4, False)
        elif self.pl.rect.center[0] > self.rect.center[0]:
            self.enter(4, -3, False)
        elif self.pl.rect.x + self.pl.rect.width - self.pl.a // 2 < self.rect.center[0]:
            self.enter(3, 4, False)
        else:
            self.enter(4, 3, False)

    def enter(self, y, x, t=True):
        if self.flight and t:
            self.pl.l()
        else:
            self.flight = True
            self.vx = (x // abs(x)) * 500 // (x ** 2 + y ** 2) * x ** 2 * 4
            self.vy = - (500 // (x ** 2 + y ** 2) * y ** 2) * 4
            self.update()
            self.update()

    def update(self):
        if not self.flight:
            self.x = self.pl.rect.x + self.pl.a * self.pl.flag // 2
            self.rect.x = self.x
            self.c[0] = self.x * 1000
        else:
            self.c[0] += self.vx
            self.c[1] += self.vy
            self.rect.x = self.c[0] // 1000
            self.rect.y = self.c[1] // 1000


class Board:
    def __init__(self, width, height, highscore):
        self._lines = pygame.sprite.Group()
        c_br = [((255, 255, 255), 1), ((255, 255, 0), 1), ((255, 0, 255), 1), ((0, 255, 255), 1), ((255, 0, 0), 1),
                ((0, 255, 0), 1), ((0, 0, 255), 1), ((200, 200, 200), 2), ((255, 215, 0), float('inf'))]
        self._ = 0  # пасхалка(при уничтожении 20 летающих врагов за уровень выполнится переход на новый уровень)
        self.go = False
        self.c = 0
        self.score = 0
        self.hs = highscore
        self.lvl = 0
        self.hr = pygame.sprite.Group()
        self.vr = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Group()
        self.width = width
        self.height = height
        self.left = 10
        self.top = 10
        self.cell_size1 = 50
        self.cell_size2 = 25
        self.p = pygame.sprite.Group()
        self.pl = Platform(self, self.cell_size1, self.cell_size1 + self.left, self.cell_size1 * 20 + self.top, self.p)
        self.pl.set_field_and_size(self.left, self.cell_size1 * width)
        self.b = pygame.sprite.Group()
        self.ball = Ball(self.cell_size1 // 16 * 5, self.cell_size1 + self.left,
                         self.cell_size1 * 20 + self.top - self.cell_size1 // 16 * 2 + 1, self.pl, self.b)
        self.vrl = [Line(self.cell_size1 // 16 * 2, self.cell_size2 * self.height,
                         self.left + self.cell_size1 // 16 * (15 + 16 * i), self.top, self.vr) for i in
                    range(-1, self.width)]
        self.hrl = [Line(self.cell_size1 * self.width, self.cell_size2 // 8 * 2, self.left,
                         self.top + self.cell_size2 // 8 * (7 + 8 * i), self.hr) for i in range(-1, self.height)]
        self.fons = [
            [Fon(self.cell_size1, i * self.cell_size1 + self.left, j * self.cell_size1 + self.top, self.fon) for i in
             range(self.width)] for j in range(self.height // 2)]
        self.board = [[random.choice([Block(self, self.cell_size1, self.cell_size2, i * self.cell_size1 + self.left,
                                            j * self.cell_size2 + self.top, self.sprites, *(random.choice(c_br))), None,
                                      None]) for i in range(self.width)] for j in range(self.height - 10)] + [
                         [None for i in range(self.width)] for j in range(10)]
        self.ls = pygame.sprite.Group()
        self.gt = pygame.sprite.Group()
        self.cs = pygame.sprite.Group()
        self.f = pygame.sprite.Group()

    def set_view(self, left, top, cell_size1, cell_size2):
        c_br = [((255, 255, 255), 1), ((255, 255, 0), 1), ((255, 0, 255), 1), ((0, 255, 255), 1), ((255, 0, 0), 1),
                ((0, 255, 0), 1), ((0, 0, 255), 1), ((200, 200, 200), 2), ((255, 215, 0), float('inf'))]
        self.left = left
        self.top = top
        self.cell_size1 = cell_size1
        self.cell_size2 = cell_size2
        self.pause = False
        self._ = 0
        for i in (self.fons + self.board):
            for j in i:
                if j is not None:
                    j.kill()
        for i in (self.vrl + self.hrl):
            i.kill()
        self.p = pygame.sprite.Group()
        self.pl = Platform(self, self.cell_size1, self.cell_size1 + self.left, self.cell_size2 * 20 + self.top, self.p)
        self.pl.set_field_and_size(self.left, self.cell_size1 * self.width)
        self.b = pygame.sprite.Group()
        self.ball = Ball(self.cell_size1 // 16 * 5, self.cell_size1 + self.left,
                         self.cell_size2 * 20 + self.top - self.cell_size2 // 8 * 6 + 3, self.pl, self.b)
        self.vrl = [Line(2, self.cell_size2 * self.height, self.left + self.cell_size1 * (i + 1) - 1, self.top, self.vr)
                    for i in range(-1, self.width)]
        self.hrl = [Line(self.cell_size1 * self.width, 2, self.left, self.top + self.cell_size2 * (i + 1) - 1, self.hr)
                    for i in range(-1, self.height)]
        self.fons = [
            [Fon(self.cell_size1, i * self.cell_size1 + self.left, j * self.cell_size1 + self.top, self.fon) for i in
             range(self.width)] for j in range(self.height // 2)]
        self.board = [[random.choice([Block(self, self.cell_size1, self.cell_size2, i * self.cell_size1 + self.left,
                                            j * self.cell_size2 + self.top, self.sprites, *(random.choice(c_br))), None,
                                      None]) for i in range(self.width)] for j in range(self.height - 10)] + [
                         [None for i in range(self.width)] for j in range(10)]
        self.ls = pygame.sprite.Group()
        self.gt = pygame.sprite.Group()
        self.cs = pygame.sprite.Group()
        self.f = pygame.sprite.Group()

    def render(self, screen):
        self._lines.draw(screen)
        if self.pause:
            return
        self.ls.update()
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] is not None:
                    if not self.board[i][j].br:
                        self.board[i][j] = None
                        continue
                    self.board[i][j].update()
                    if pygame.sprite.spritecollide(self.board[i][j], self.b, False):
                        self.board[i][j]._ball(self.ball)
                        self.board[i][j].collide__()
                        if self.ball.flag:
                            self.board[i][j].collide__()
                    if pygame.sprite.spritecollide(self.board[i][j], self.ls, True):
                        self.board[i][j].collide__()
                        self.upscore(10)
        self.ball.update()
        if pygame.sprite.spritecollide(self.ball, self.p, False):
            self.upscore(10)
            self.ball.platformhit()
            self.ball.update()
        if pygame.sprite.spritecollide(self.ball, self.gt, True):
            self.upscore(10)
            self.ball.platformhit()
            self.ball.update()
        if pygame.sprite.collide_mask(self.ball, self.vrl[0]):
            self.upscore(10)
            self.ball.vx = abs(self.ball.vx)
            self.ball.update()
        if pygame.sprite.collide_mask(self.ball, self.vrl[-1]):
            self.upscore(10)
            self.ball.vx = - abs(self.ball.vx)
            self.ball.update()
        if pygame.sprite.collide_mask(self.ball, self.hrl[0]):
            self.upscore(10)
            self.ball.vy = abs(self.ball.vy)
            self.ball.update()
        if pygame.sprite.collide_mask(self.ball, self.hrl[-1]):
            self.upscore(10)
            if TEST:
                self.ball.vy = - abs(self.ball.vy)
            else:
                self.c -= 1
                self.ball.vy = - abs(self.ball.vy)
                if self.c < 0:
                    self.go = True
        pygame.sprite.spritecollide(self.hrl[0], self.ls, True)
        sc = pygame.sprite.spritecollide(self.pl, self.cs, True)
        if pygame.sprite.groupcollide(self.ls, self.f, True, True):
            self.upscore(50)
            self._ += 5
            if self._ >= 100:
                self._ = 0
                self.lvl += 1
                random.seed(self.lvl)
                self.set_view(self.left, self.top, self.cell_size1, self.cell_size2)
                self.upscore(2000)
                return
        for i in sc:
            i.____(self)
        pygame.sprite.spritecollide(self.vrl[0], self.f, True)
        pygame.sprite.spritecollide(self.vrl[-1], self.f, True)
        pygame.sprite.spritecollide(self.hrl[0], self.f, True)
        pygame.sprite.spritecollide(self.hrl[-1], self.f, True)
        pygame.sprite.spritecollide(self.hrl[-1], self.cs, True)
        if pygame.sprite.spritecollide(self.ball, self.f, True):
            self.upscore(50)
            self.ball.vy = abs(self.ball.vy)
            self._ += 5
            if self._ >= 100:
                self._ = 0
                self.lvl += 1
                random.seed(self.lvl)
                self.set_view(self.left, self.top, self.cell_size1, self.cell_size2)
                self.upscore(2000)
                return
        self.hr.draw(screen)
        self.vr.draw(screen)
        self.pl.update(pygame.mouse.get_pos()[0])
        self.ball.update()
        self.fon.draw(screen)
        self.ls.draw(screen)
        self.sprites.draw(screen)
        self.p.draw(screen)
        self.b.draw(screen)
        self.cs.update()
        self.cs.draw(screen)
        self.gt.draw(screen)
        if not random.randint(0, 1024):
            FlyingOpponent(self)
        self.f.update()
        self.f.draw(screen)
        if self.go:
            global running
            running = False

        flag = True
        for i in self.board:
            for j in i:
                if j is not None:
                    if j.br > 0 and j.br != float('inf'):
                        flag = False
        if flag:
            self.lvl += 1
            random.seed(self.lvl)
            self.set_view(self.left, self.top, self.cell_size1, self.cell_size2)
            self._ = 0
            return

        txt = pygame.font.Font(None, 50).render(f'HIGHSCORE', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 100)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 100))
        txt = pygame.font.Font(None, 50).render(f'{self.hs}', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 150)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 150))
        txt = pygame.font.Font(None, 50).render(f'SCORE', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 200)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 200))
        txt = pygame.font.Font(None, 50).render(f'{self.score}', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 250)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 250))
        txt = pygame.font.Font(None, 50).render(f'LEVEL', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 300)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 300))
        txt = pygame.font.Font(None, 50).render(f'{self.lvl}', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 350)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 350))
        self.txt = pygame.font.Font(None, 50).render('PAUSE', True, (255, 255, 255))
        self.r = self.txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 400)
        screen.blit(self.txt, (self.left + self.width * self.cell_size1 + 50, 400))
        txt = pygame.font.Font(None, 50).render(f'{self.c}', True, (255, 255, 255))
        r = txt.get_rect().move(self.left + self.width * self.cell_size1 + 50, 450)
        screen.blit(txt, (self.left + self.width * self.cell_size1 + 50, 450))
        g = pygame.sprite.Group()
        Platform(self, self.cell_size1, self.left + self.width * self.cell_size1 + 150, 450, g)
        g.draw(screen)

    def upscore(self, n):
        self.score += n
        self.hs = max(self.hs, self.score)

    def get_click(self, mouse_pos):
        self.ball.enter(4, 3)
        if pygame.mouse.get_pos()[0] > self.left + self.width * self.cell_size1 + 50 and pygame.mouse.get_pos()[
            0] < self.left + self.width * self.cell_size1 + 50 + self.r.width:
            if pygame.mouse.get_pos()[1] > 400 and pygame.mouse.get_pos()[1] < 400 + self.r.height:
                self.pause = not self.pause


pygame.init()
pygame.display.set_caption('Arkanoid')
pygame.display.set_icon(Ball(16, -1000, -1000, Platform(Board(2, 2, 0), 16, -1000, -1000, pygame.sprite.Group()),
                             pygame.sprite.Group()).image)
clock = pygame.time.Clock()
r = True
try:
    f = open('hs', 'r')
except:
    class __:
        def read(self):
            return '0'

        def close(self):
            del self


    f = __()
board = Board(10, 24, int(f.read()))
try:
    f = open('s&l', 'r')
except:
    class __:
        def read(self):
            return '0 0 0'

        def close(self):
            del self


    f = __()
board.c = int(f.read().split()[0])
try:
    f = open('s&l', 'r')
except:
    class __:
        def read(self):
            return '0 0 0'

        def close(self):
            del self

        f = __()
board.lvl = int(f.read().split()[1])
try:
    f = open('s&l', 'r')
except:
    class __:
        def read(self):
            return '0 0 0'

        def close(self):
            del self

        f = __()
board.score = int(f.read().split()[2])
lvl = board.lvl
f.close()
while r:
    running = True
    screen = pygame.display.set_mode((800, 640))
    while running:
        screen.fill((0, 0, 255))
        txt = pygame.font.Font(None, 100).render('ARKANOID', True, (255, 0, 0))
        a1 = txt.get_rect().move(200, 150)
        screen.blit(txt, (210, 150))
        col = tuple([random.randint(0, 255) for _ in range(3)])
        txt = pygame.font.Font(None, 50).render('Start game.', True, col)
        a2 = txt.get_rect().move(300, 250)
        screen.blit(txt, (300, 250))
        txt = pygame.font.Font(None, 50).render('Press any key', True, col)
        a3 = txt.get_rect().move(285, 300)
        screen.blit(txt, (285, 300))
        txt = pygame.font.Font(None, 50).render('or click', True, col)
        a4 = txt.get_rect().move(300, 350)
        screen.blit(txt, (335, 350))
        txt = pygame.font.Font(None, 50).render('to continue.', True, col)
        a5 = txt.get_rect().move(300, 400)
        screen.blit(txt, (300, 400))
        txt = pygame.font.Font(None, 50).render('Press R to reset', True, col)
        a6 = txt.get_rect().move(270, 450)
        screen.blit(txt, (260, 450))
        time.sleep(0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.unicode == 'r':
                    open('hs', 'w').write('0')
                    board.hs = 0
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False
                break
        pygame.display.flip()
    if not r:
        continue
    running = True
    random.seed(lvl)
    board = Board(10, 24, board.hs)
    board.go = False
    try:
        f = open('s&l', 'r')
    except:
        class __:
            def read(self):
                return '0 0 0'

            def close(self):
                del self


        f = __()
    board.c = int(f.read().split()[0])
    try:
        f = open('s&l', 'r')
    except:
        class __:
            def read(self):
                return '0 0 0'

            def close(self):
                del self


        f = __()
    board.lvl = int(f.read().split()[1])
    try:
        f = open('s&l', 'r')
    except:
        class __:
            def read(self):
                return '0 0 0'

            def close(self):
                del self


        f = __()
    board.score = int(f.read().split()[2])
    lvl = board.lvl
    f.close()
    board.set_view(50, 50, 48, 24)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                r = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        if not board.pause:
            screen.fill((0, 0, 0))
            board.render(screen)
            pygame.display.flip()
        clock.tick(80)
    open('hs', 'w').write(str(board.hs))
    if not board.go:
        open('s&l', 'w').write(' '.join([str(board.c), str(board.lvl), str(board.score)]))
    if not r:
        continue
    running = True
    for i in range(8):
        screen.fill((0, 0, 0))
        pygame.event.get()
        col = tuple([random.randint(0, 255) for _ in range(3)])
        txt = pygame.font.Font(None, 50).render('Game Over!', True, col)
        a7 = txt.get_rect().move(300, 300)
        screen.blit(txt, (300, 300))
        time.sleep(0.5)
        pygame.display.flip()
pygame.quit()
