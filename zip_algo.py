import os
import cv2
from board_reader import detect_board, GRID_W, GRID_H, Point

INPUT_IMAGE = "puzzle_1.png"
OUTPUT_IMAGE = "solved.png"


def print_board(board):
    hwalls = set()
    for seg in board.h_walls:
        y = seg.start.y
        for x in range(min(seg.start.x, seg.end.x), max(seg.start.x, seg.end.x)):
            hwalls.add((x, y))
    vwalls = set()
    for seg in board.v_walls:
        x = seg.start.x
        for y in range(min(seg.start.y, seg.end.y), max(seg.start.y, seg.end.y)):
            vwalls.add((x, y))
    label_at = {(p.x, p.y): n for n, p in board.label_map.items()}
    for y in range(board.height + 1):
        row = ""
        for x in range(board.width):
            row += "+" + ("---" if (x, y) in hwalls else "   ")
        row += "+"
        print(row)
        if y < board.height:
            row = ""
            for x in range(board.width + 1):
                row += "|" if (x, y) in vwalls else " "
                if x < board.width:
                    val = label_at.get((x, y), " ")
                    row += str(val).center(3)
            print(row)
    print()


def print_path(path, board):
    grid = [[" ." for _ in range(board.width)] for _ in range(board.height)]
    for idx, p in enumerate(path, start=1):
        grid[p.y][p.x] = f"{idx:2d}"
    for row in grid:
        print("".join(cell for cell in row))
    print()


def solve(image_path=INPUT_IMAGE, output_path=OUTPUT_IMAGE):
    board = detect_board(image_path)
    print_board(board)
    labels = sorted(board.label_map)
    points = [board.label_map[n] for n in labels]
    label_positions = {p: idx for idx, p in enumerate(points)}
    blocked = set()
    for seg in board.h_walls:
        y0 = seg.start.y
        for x in range(min(seg.start.x, seg.end.x), max(seg.start.x, seg.end.x)):
            blocked.add(((x, y0 - 1), (x, y0)))
            blocked.add(((x, y0), (x, y0 - 1)))
    for seg in board.v_walls:
        x0 = seg.start.x
        for y in range(min(seg.start.y, seg.end.y), max(seg.start.y, seg.end.y)):
            blocked.add(((x0 - 1, y), (x0, y)))
            blocked.add(((x0, y), (x0 - 1, y)))
    start = points[0]
    path = [start]
    visited = {start}

    def dfs(cell, next_idx):
        if cell in label_positions:
            idx = label_positions[cell]
            if idx != next_idx:
                return False
            next_idx += 1
        if len(path) == GRID_W * GRID_H:
            return True
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = cell.x + dx, cell.y + dy
            nxt = Point(nx, ny)
            if not (0 <= nx < GRID_W and 0 <= ny < GRID_H):
                continue
            if ((cell.x, cell.y), (nx, ny)) in blocked or nxt in visited:
                continue
            visited.add(nxt)
            path.append(nxt)
            if dfs(nxt, next_idx):
                return True
            path.pop()
            visited.remove(nxt)
        return False

    found = dfs(start, 0)
    if not found:
        print("No solution found")
        return
    print("Solution path indices:")
    print_path(path, board)

    img = cv2.imread(image_path)
    h_img, w_img = img.shape[:2]
    cw = w_img / GRID_W
    ch = h_img / GRID_H
    for a, b in zip(path, path[1:]):
        p1 = (int((a.x + 0.5) * cw), int((a.y + 0.5) * ch))
        p2 = (int((b.x + 0.5) * cw), int((b.y + 0.5) * ch))
        cv2.line(img, p1, p2, (0, 255, 0), 2)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    cv2.imwrite(output_path, img)
    print(f"Solution image saved as {output_path}")


if __name__ == "__main__":
    solve()
