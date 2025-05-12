import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
from collections import namedtuple
import os

GRID_W, GRID_H = 6, 6
Point = namedtuple("Point", ["x", "y"])
Segment = namedtuple("Segment", ["start", "end"])


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.h_walls = []
        self.v_walls = []
        self.label_map = {}


def detect_board(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image {path!r}")

    debug_img = img.copy()
    h_img, w_img = img.shape[:2]
    cell_w = w_img / GRID_W
    cell_h = h_img / GRID_H
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    clean = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel, iterations=2)

    board = Board(GRID_W, GRID_H)

    hor_k = cv2.getStructuringElement(cv2.MORPH_RECT, (int(cell_w * 0.8), 3))
    hor = cv2.morphologyEx(clean, cv2.MORPH_OPEN, hor_k, iterations=1)
    cnts, _ = cv2.findContours(hor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        x, y, w1, h1 = cv2.boundingRect(c)
        if w1 < cell_w * 0.4:
            continue
        x1 = round(x / cell_w)
        x2 = round((x + w1) / cell_w)
        y0 = round((y + h1 / 2) / cell_h)
        board.h_walls.append(Segment(Point(x1, y0), Point(x2, y0)))
        cv2.rectangle(debug_img, (x, y), (x + w1, y + h1), (0, 0, 255), 2)

    ver_k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, int(cell_h * 0.8)))
    ver = cv2.morphologyEx(clean, cv2.MORPH_OPEN, ver_k, iterations=1)
    cnts, _ = cv2.findContours(ver, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        x, y, w1, h1 = cv2.boundingRect(c)
        if h1 < cell_h * 0.4:
            continue
        x0 = round((x + w1 / 2) / cell_w)
        y1 = round(y / cell_h)
        y2 = round((y + h1) / cell_h)
        board.v_walls.append(Segment(Point(x0, y1), Point(x0, y2)))
        cv2.rectangle(debug_img, (x, y), (x + w1, y + h1), (0, 0, 255), 2)

    walls_mask = cv2.bitwise_or(hor, ver)
    blob_mask = cv2.subtract(clean, walls_mask)
    hole_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    blob_mask = cv2.morphologyEx(blob_mask, cv2.MORPH_CLOSE, hole_k, iterations=2)

    cnts, _ = cv2.findContours(blob_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        x, y, w1, h1 = cv2.boundingRect(c)
        if w1 < cell_w * 0.3 or h1 < cell_h * 0.3:
            continue
        cx, cy = x + w1 / 2, y + h1 / 2
        gx, gy = int(cx / cell_w), int(cy / cell_h)
        pad = int(min(w1, h1) * 0.2)
        x0 = max(int(cx - w1 / 2) + pad, 0)
        y0 = max(int(cy - h1 / 2) + pad, 0)
        x1 = min(int(cx + w1 / 2) - pad, w_img)
        y1 = min(int(cy + h1 / 2) - pad, h_img)
        if x1 <= x0 or y1 <= y0:
            continue
        roi = gray[y0:y1, x0:x1]
        roi = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, thr = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        er_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thr = cv2.erode(thr, er_k, iterations=1)
        pil_img = Image.fromarray(thr)
        data = pytesseract.image_to_data(
            pil_img,
            output_type=Output.DICT,
            config="--psm 10 -c tessedit_char_whitelist=0123456789",
        )
        best_num, best_conf = None, -1
        for txt, conf in zip(data["text"], data["conf"]):
            if txt.isdigit() and int(conf) > best_conf:
                best_conf = int(conf)
                best_num = int(txt)
        if best_num is not None:
            board.label_map[best_num] = Point(gx, gy)
            cv2.rectangle(debug_img, (x0, y0), (x1, y1), (0, 255, 0), 2)
            cv2.putText(
                debug_img,
                str(best_num),
                (x0, y0 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2,
            )

    print("Detected labels and grid positions:")
    for num in sorted(board.label_map):
        p = board.label_map[num]
        print(f"{num}: ({p.x}, {p.y})")

    debug_path = os.path.splitext(path)[0] + "_detected.png"
    cv2.imwrite(debug_path, debug_img)
    return board
