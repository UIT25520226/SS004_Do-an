# Rotation — Xoay block Tetris

## Cách dùng

Trong `CodeTetris.py`, thêm:

```python
from Rotation.Rotation import rotateBlock
```

Khi nhấn `w` (sau `boardDelBlock()`):

```python
if c == 'w':
    rotateBlock(currentBlock, board, x, y)
```

Dùng `currentBlock = blocks[b].copy()` mỗi lần sinh khối mới. Ba hàm `canMove()`, `block2Board()`, `boardDelBlock()` đọc `currentBlock[i][j]` thay cho `blocks[b][i][j]`.

## Logic xoay

1. Xoay ma trận 4×4 sang phải 90°: `(i, j) → (j, 3 - i)`.
2. Kiểm tra biên bàn chơi và các khối đã nằm trên `board`. Nếu vướng thì giữ nguyên khối.
3. Nếu không vướng, cập nhật `currentBlock` và trả về `True`.

`boardDelBlock()` phải chạy trước khi gọi hàm xoay.
