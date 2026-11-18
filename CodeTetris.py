import random
import pygame

H = 20
W = 15
CELL = 30  # kích thước 1 ô (pixel)

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
            if blocks[b][i][j] != ' ':
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
            if blocks[b][i][j] != ' ':
                board[y + i][x + j] = blocks[b][i][j]


def boardDelBlock():
    for i in range(4):
        for j in range(4):
            if blocks[b][i][j] != ' ':
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


def removeLine():
    i = H - 2
    while i > 0:
        j = 0
        while j < W:
            if board[i][j] == ' ':
                break
            j += 1
        if j == W:
            for ii in range(i, 0, -1):
                for jj in range(W):
                    board[ii][jj] = board[ii - 1][jj]
            i += 1
            draw()
            pygame.event.pump()
            pygame.time.delay(200)  # _sleep(200)
        i -= 1


def main():
    global x, y, b, screen, font
    pygame.init()
    screen = pygame.display.set_mode((W * CELL, H * CELL))
    pygame.display.set_caption("Tetris")
    font = pygame.font.SysFont("consolas", 20, bold=True)
    clock = pygame.time.Clock()

    x = 5
    y = 0
    b = random.randrange(7)  # giữ nguyên như code gốc: rand() % 7
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
                if c == 'q':
                    running = False

        # tương đương _sleep(500): cứ 500ms thì khối rơi 1 ô
        now = pygame.time.get_ticks()
        if now - last_drop >= 500:
            last_drop = now
            if canMove(0, 1):
                y += 1
            else:
                block2Board()
                removeLine()
                x = 5
                y = 0
                b = random.randrange(7)

        block2Board()
        draw()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
