import random
import time
import numpy as np

"""
matrix : 0 is covered, 1 is uncovered.
items : [(width,height,num)]
        e.g. [(1, 2, 4), (2, 3, 1)] means you have 4 items of (1,2) shape , 1 items of (2,3) shape.
MAX_SOLUTIONS : Default value is 3000. The higher the value, the more accurate the result.
"""

matrix = np.array([
    [0, 0, 1, 1, 0, 1, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 1, 1, 1, 1, 1]
])
items = [(1, 2, 4)]
MAX_SOLUTIONS = 10000
USE_PREFIX_MATRIX = False

"""
matrix = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
])
"""

""" Don‘t Modify """
PRINT_SOLUTIONS = False
rows, cols = matrix.shape
prob_matrix = np.zeros_like(matrix, dtype=float)


def compute_prefix_sum():
    """计算矩阵的前缀和"""
    global matrix, rows, cols
    prefix_sum = np.zeros((rows + 1, cols + 1), dtype=int)
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            prefix_sum[r, c] = matrix[r - 1, c - 1] + prefix_sum[r - 1, c] + \
                               prefix_sum[r, c - 1] - prefix_sum[r - 1, c - 1]
    return prefix_sum


def get_submatrix_sum(prefix_sum, top_left, bottom_right):
    """快速计算子矩阵的和"""
    r1, c1 = top_left
    r2, c2 = bottom_right
    return (prefix_sum[r2 + 1, c2 + 1] - prefix_sum[r2 + 1, c1] -
            prefix_sum[r1, c2 + 1] + prefix_sum[r1, c1])


def can_place1(prefix_sum, item_shape, top_left):
    """使用前缀和检查是否可以在指定位置放置房屋"""
    global matrix, rows, cols
    r, c = top_left
    item_rows, item_cols = item_shape
    bottom_right = (r + item_rows - 1, c + item_cols - 1)
    if bottom_right[0] >= rows or bottom_right[1] >= cols:
        return False
    submatrix_sum = get_submatrix_sum(prefix_sum, top_left, bottom_right)
    return submatrix_sum == 0


def can_place2(house, top_left):
    h_rows, h_cols = house
    r, c = top_left
    if r + h_rows > rows or c + h_cols > cols:
        return False
    for i in range(h_rows):
        for j in range(h_cols):
            if matrix[r + i][c + j] != 0:
                return False
    return True


def place_item(item_shape, top_left, item_id):
    """在指定位置放置房屋"""
    global matrix
    r, c = top_left
    item_rows, item_cols = item_shape
    for i in range(item_rows):
        for j in range(item_cols):
            matrix[r + i, c + j] = item_id  # 使用不同的数字表示不同种类的房屋


def remove_item(item_shape, top_left):
    """移除指定位置的房屋"""
    global matrix
    r, c = top_left
    item_rows, item_cols = item_shape
    for i in range(item_rows):
        for j in range(item_cols):
            matrix[r + i, c + j] = 0  # 恢复为平地


def find_single_solution(index):
    """递归地寻找单个摆放方案"""

    global items, matrix, prob_matrix
    if index >= len(items):
        if PRINT_SOLUTIONS:
            print(f"{visualize_solution()}")
        prob_matrix += np.where(matrix >= 2, 1, 0)
        return True

    prefix_sum = None
    item_id = index + 2  # 使用下标作为item_id
    item_shape = items[index]
    rotations = [item_shape, item_shape[::-1]]

    rows, cols = matrix.shape
    all_positions = [(r, c) for r in range(rows) for c in range(cols)][:-1]
    random.shuffle(all_positions)

    for r, c in all_positions:
        for rotation in rotations:
            if USE_PREFIX_MATRIX:
                if prefix_sum is None:
                    prefix_sum = compute_prefix_sum()
                tmp = can_place1(prefix_sum, rotation, (r, c))
            else:
                tmp = can_place2(rotation, (r, c))
            if tmp:
                place_item(rotation, (r, c), item_id)
                result = find_single_solution(index + 1)
                remove_item(rotation, (r, c))
                if result:
                    return True
    return False


def visualize_solution():
    """可视化单个解法"""
    global matrix
    vis_str = ""
    for row in matrix:
        vis_str += "".join([str(cell) if cell > 0 else '.' for cell in row]) + "\n"
    return vis_str


def print_matrix(matrix):
    max_value = np.max(matrix)
    for row in matrix:
        for value in row:
            if value == max_value:
                print(f"\033[1;31m{value:.2f}\033[0m", end=" ")
            else:
                print(f"{value:.2f}", end=" ")
        print()


if __name__ == "__main__":
    print(f"剩余贴纸个数：{rows * cols - np.sum(matrix)}")
    items = [(h, w) for h, w, n in items for _ in range(n)]
    items = sorted(items, key=lambda x: x[0] * x[1], reverse=True)

    start_time = time.time()
    for _ in range(MAX_SOLUTIONS):
        find_single_solution(0)
    end_time = time.time()

    prob_matrix /= MAX_SOLUTIONS
    print_matrix(prob_matrix)
    print(f"耗时: {end_time - start_time} 秒") 
