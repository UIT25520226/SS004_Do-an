import random
import pygame
from Rotation.Rotation import rotateBlock


SHAPES = {
    "I": ["    ", "IIII", "    ", "    "],
    "O": ["    ", " OO ", " OO ", "    "],
    "T": ["    ", " T  ", "TTT ", "    "],
    "S": ["    ", " SS ", "SS  ", "    "],
    "Z": ["    ", "ZZ  ", " ZZ ", "    "],
    "J": ["    ", "J   ", "JJJ ", "    "],
    "L": ["    ", "  L ", "LLL ", "    "],
}

class Block:
    def __init__(self, kind, x=5, y=0):
        self.kind = kind                  # "I", "O", "T", "S", "Z", "J", "L"
        self.x = x                        # cột góc trái trên của ma trận 4x4
        self.y = y                        # hàng góc trái trên của ma trận 4x4
        self.shape = list(SHAPES[kind])   # copy để không sửa SHAPES gốc
    def cells(self): ...          # trả về list (hàng, cột, ký tự) các ô có khối
    def rotated(self): ...        # trả về shape mới sau khi xoay phải 90 độ (không sửa self)
    def rotate(self, board): ...  # xoay nếu board.can_place cho phép, trả về True/False


class Board:
    def __init__(self, w=15, h=20):
        self.w = w
        self.h = h
        # lưới có tường '#' ở viền, bên trong là ' ' (giống initBoard cũ)
        self.grid = [[' '] * w for _ in range(h)]
        for i in range(h):
            for j in range(w):
                if i == 0 or i == h - 1 or j == 0 or j == w - 1:
                    self.grid[i][j] = '#'

    def can_place(self, block, dx=0, dy=0, shape=None):
        # True nếu khối (dịch dx, dy, và dùng shape nếu có) không vướng tường hay ô đã đặt
        target_shape = shape if shape is not None else block.shape
        for i in range(4):
            for j in range(4):
                if target_shape[i][j] != ' ':
                    xt = block.x + j + dx
                    yt = block.y + i + dy
                    if not (1 <= xt < self.w - 1 and 0 <= yt < self.h - 1):
                        return False
                    if self.grid[yt][xt] != ' ':
                        return False
        return True

    def place(self, block):
        # ghi khối vào lưới khi chạm đáy
        for i in range(4):
            for j in range(4):
                if block.shape[i][j] != ' ':
                    self.grid[block.y + i][block.x + j] = block.shape[i][j]

    def clear_lines(self):
        # xóa các dòng đầy, trả về số dòng đã xóa
        removed = 0
        i = self.h - 2
        while i > 0:
            if all(self.grid[i][j] != ' ' for j in range(1, self.w - 1)):
                removed += 1
                for ii in range(i, 1, -1):
                    for jj in range(1, self.w - 1):
                        self.grid[ii][jj] = self.grid[ii - 1][jj]
                for jj in range(1, self.w - 1):
                    self.grid[1][jj] = ' '
                i += 1          # kiểm tra lại dòng này vì vừa có dòng mới dồn xuống
            i -= 1
        return removed


class ScoreManager:
    def __init__(self): ...            # score = 0, drop_interval = 500
    def add_lines(self, lines): ...    # cộng điểm + tăng tốc
    # thuộc tính: score, drop_interval


class Renderer:
    def __init__(self, board): ...
    def draw(self, board, block, score): ...   # vẽ board, rồi block, rồi điểm


class Game:
    def __init__(self): ...
    def handle_input(self): ...
    def update(self): ...              # rơi, chạm đáy, sinh khối mới
    def run(self): ...
H = 20
W = 15
CELL = 30  # kích thước 1 ô (pixel)
DROP_INTERVAL = 500       # Thời gian giữa mỗi lần rơi (ms)
MIN_DROP_INTERVAL = 80    # Tốc độ rơi tối đa
SPEEDUP_PER_LINE = 35     # Giảm 35 ms mỗi dòng được xóa

board = [[' '] * W for _ in range(H)]

x = y = b = 0
blocks = [
    [" I  ",
     " I  ",
     " I  ",
     " I  "],
    [" I  ",
     " I  ",
     " I  ",
     " I  "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     "IIII",
     "    ",
     "    "],
    ["    ",
     " OO ",
     " OO ",
     "    "],
    ["    ",
     " T  ",
     "TTT ",
     "    "],
    ["    ",
     " SS ",
     "SS  ",
     "    "],
    ["    ",
     "ZZ  ",
     " ZZ ",
     "    "],
    ["    ",
     "J   ",
     "JJJ ",
     "    "],
    ["    ",
     "  L ",
     "LLL ",
     "    "],
]

currentBlock = []

# Màu cho từng ký tự (thay cho việc in ký tự ra console)
COLORS = {
    '#': (110, 110, 110),
    'I': (0, 240, 240),
    'O': (240, 240, 0),
    'T': (160, 0, 240),
    'S': (0, 240, 0),
    'Z': (240, 0, 0),
    'J': (0, 0, 240),
    'L': (240, 160, 0),
}
# ===================== TÍNH ĐIỂM =====================
score = 0
# Số điểm theo số dòng xóa cùng lúc (kiểu Tetris cổ điển)
LINE_SCORES = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}


def countFullLines():
    #Đếm số dòng đã đầy trên board (gọi TRƯỚC removeLine).
    count = 0
    for i in range(1, H - 1):
        if all(board[i][j] != ' ' for j in range(W)):
            count += 1
    return count

def addScore(lines):
    #Cộng điểm theo số dòng vừa xóa và cập nhật tiêu đề cửa sổ.
    global score
    score += LINE_SCORES.get(lines, 0)
    pygame.display.set_caption(f"Tetris - Score: {score}")


screen = None
font = None


def canMove(dx, dy):
    for i in range(4):
        for j in range(4):
            if currentBlock[i][j] != ' ':
                xt = x + j + dx
                yt = y + i + dy
                if xt < 1 or xt >= W - 1 or yt >= H - 1:
                    return False
                if board[yt][xt] != ' ':
                    return False
    return True


def block2Board():
    for i in range(4):
        for j in range(4):
            if currentBlock[i][j] != ' ':
                board[y + i][x + j] = currentBlock[i][j]


def boardDelBlock():
    for i in range(4):
        for j in range(4):
            if currentBlock[i][j] != ' ':
                board[y + i][x + j] = ' '


def initBoard():
    for i in range(H):
        for j in range(W):
            if i == 0 or i == H - 1 or j == 0 or j == W - 1:
                board[i][j] = '#'
            else:
                board[i][j] = ' '


def draw():
    # tương đương system("cls") + in board
    screen.fill((0, 0, 0))
    for i in range(H):
        for j in range(W):
            c = board[i][j]
            if c != ' ':
                rect = pygame.Rect(j * CELL, i * CELL, CELL, CELL)
                pygame.draw.rect(screen, COLORS[c], rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                text = font.render(c, True, (0, 0, 0))
                screen.blit(text, text.get_rect(center=rect.center))
    pygame.display.flip()
# ===================== GIAO DIỆN Ô VUÔNG =====================
def draw():
    screen.fill((0, 0, 0))
    for i in range(H):
        for j in range(W):
            c = board[i][j]
            if c == ' ':
                continue
            px, py = j * CELL, i * CELL
            color = COLORS[c]

            # nền ô (chừa 1 pixel mỗi cạnh để các ô tách nhau rõ)
            pygame.draw.rect(screen, color, (px + 1, py + 1, CELL - 2, CELL - 2))

            # viền sáng bên trong cho ra dạng khối nổi (bỏ qua tường '#')
            if c != '#':
                light = tuple(min(255, v + 70) for v in color)
                pygame.draw.rect(screen, light,
                                 (px + 3, py + 3, CELL - 6, CELL - 6), 2)
    pygame.display.flip()
# =============================================================

def removeLine():
    global DROP_INTERVAL

    removed_lines = 0
    i = H - 2

    while i > 0:
        if all(board[i][j] != ' ' for j in range(1, W - 1)):
            removed_lines += 1

            for ii in range(i, 1, -1):
                for jj in range(1, W - 1):
                    board[ii][jj] = board[ii - 1][jj]

            for jj in range(1, W - 1):
                board[1][jj] = ' '

            draw()
            pygame.event.pump()
            pygame.time.delay(200)

            i += 1

        i -= 1

    # Tăng tốc độ rơi dựa trên số dòng vừa xóa
    if removed_lines > 0:
        DROP_INTERVAL = max(
            MIN_DROP_INTERVAL,
            DROP_INTERVAL - SPEEDUP_PER_LINE * removed_lines
        )

    return removed_lines

def main():
    global x, y, b, screen, font, currentBlock
    pygame.init()
    screen = pygame.display.set_mode((W * CELL, H * CELL))
    pygame.display.set_caption("Tetris")
    font = pygame.font.SysFont("consolas", 20, bold=True)
    clock = pygame.time.Clock()

    x = 5
    y = 0
    b = random.randrange(9, 16)  # I, O, T, S, Z, J, L
    currentBlock = blocks[b].copy()
    initBoard()

    last_drop = pygame.time.get_ticks()
    running = True
    while running:
        boardDelBlock()

        # tương đương kbhit() / getch()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                c = event.unicode
                if c == 'a' and canMove(-1, 0):
                    x -= 1
                if c == 'd' and canMove(1, 0):
                    x += 1
                if c == 'x' and canMove(0, 1):
                    y += 1
                if c == 'w':
                    rotateBlock(currentBlock, board, x, y)
                if c == 'q':
                    running = False

        # tương đương _sleep(500): cứ 500ms thì khối rơi 1 ô
        now = pygame.time.get_ticks()
        if now - last_drop >= DROP_INTERVAL:
            last_drop = now
            if canMove(0, 1):
                y += 1
            else:
                block2Board()

                lines_removed = removeLine()
                addScore(lines_removed)

                x = 5
                y = 0
                b = random.randrange(9, 16)
                currentBlock = blocks[b].copy()

        block2Board()
        draw()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
