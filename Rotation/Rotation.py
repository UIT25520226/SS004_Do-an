def rotateBlock(block, board, x, y):
    # Xoay ma trận 4x4 sang phải 90 độ.
    rotated = [[' '] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            rotated[j][3 - i] = block[i][j]

    newBlock = [''.join(row) for row in rotated]
    H = len(board)
    W = len(board[0])

    # Kiểm tra khối sau xoay có đụng tường hoặc khối khác không.
    for i in range(4):
        for j in range(4):
            if newBlock[i][j] == ' ':
                continue

            xt = x + j
            yt = y + i
            if xt < 1 or xt >= W - 1 or yt < 1 or yt >= H - 1:
                return False
            if board[yt][xt] != ' ':
                return False

    # Không vướng thì cập nhật khối đang rơi.
    block[:] = newBlock
    return True
