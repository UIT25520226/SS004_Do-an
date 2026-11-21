# Rotation.h — Xoay block trong Tetris

## 1. Cách dùng

Trong `CodeTetris.cpp` ở thư mục gốc, thêm:

```cpp
#include "Rotation/Rotation.h"
```

Khai báo `char currentBlock[4][4];` và sao chép `blocks[b]` vào mảng này mỗi khi tạo block mới. Trong `canMove()`, `block2Board()`, `boardDelBlock()`, đổi `blocks[b][i][j]` thành `currentBlock[i][j]`.

Khi xử lý phím `w` (sau `boardDelBlock()`):

```cpp
if (c == 'w') {
    tetris::tryRotateClockwise(currentBlock, board, x, y);
}
```

## 2. Logic xoay

1. Tạo ma trận `rotated[4][4]`. Xoay 90° theo chiều kim đồng hồ bằng công thức `rotated[j][3 - i] = shape[i][j]`.
2. Kiểm tra từng ô khác `' '`: nếu vượt biên hoặc đụng khối đã nằm trên `board` thì trả `false`, không xoay.
3. Nếu tất cả ô đều hợp lệ, chép `rotated` vào `shape` và trả `true`.

Hàm chỉ xoay hình, không đổi `x`, `y` hay `board`.
