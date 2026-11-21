#ifndef TETRIS_ROTATION_H
#define TETRIS_ROTATION_H

#include <cstddef>

namespace tetris {

// Xoay khối 4x4 sang phải 90 độ.
// Trước khi gọi, cần xóa khối đang rơi khỏi board.
// Nếu không xoay được thì giữ nguyên khối và trả về false.
template <std::size_t Height, std::size_t Width>
bool tryRotateClockwise(char (&shape)[4][4],
                        const char (&board)[Height][Width],
                        int x, int y) {
    char rotated[4][4];

    // Tạo hình sau khi xoay.
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            rotated[j][3 - i] = shape[i][j];
        }
    }

    // Kiểm tra các ô của hình mới có vướng tường hoặc khối khác không.
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            if (rotated[i][j] == ' ') continue;

            int xt = x + j;
            int yt = y + i;

            if (xt < 1 || xt >= static_cast<int>(Width) - 1 ||
                yt < 1 || yt >= static_cast<int>(Height) - 1) {
                return false;
            }
            if (board[yt][xt] != ' ') {
                return false;
            }
        }
    }

    // Hợp lệ thì cập nhật hình đang rơi.
    for (int i = 0; i < 4; ++i) {
        for (int j = 0; j < 4; ++j) {
            shape[i][j] = rotated[i][j];
        }
    }
    return true;
}

} // namespace tetris

#endif // TETRIS_ROTATION_H
