from pathlib import Path
import re

import cv2
import numpy as np
from rapidocr import RapidOCR

OCR_ENGINE = RapidOCR()
SAVE_PREPROCESS_DEBUG_IMAGE = True
# True 時會在原圖旁輸出 *_processed.png；不需要除錯圖時設為 False。


def preprocess(filePath):
    img = cv2.imread(filePath)
    if img is None:
        raise ValueError(f"無法讀取圖片：{filePath}")
    dst = cv2.fastNlMeansDenoisingColored(img, None, 30, 30, 7, 21) # 去雜點，30為去雜點的力度

    # 將圖片顏色二元化(黑白)，127為門檻值，亮度高於127的設為255，低於127的設為0
    _, thresh = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY_INV)

    imgArr = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    yPixelLen, xPixelLen = imgArr.shape

    newImg = imgArr.copy()
    edge_width = 5
    if xPixelLen > edge_width * 2:
        # Each edge column contributes one median point, so thick strokes do not
        # receive more weight than thin ones.
        edge_x = np.r_[0:edge_width, xPixelLen - edge_width:xPixelLen]
        edge_y = []
        edge_x_valid = []
        for x in edge_x:
            rows = np.flatnonzero(imgArr[:, x] == 255)
            if rows.size:
                edge_x_valid.append(x)
                edge_y.append(float(np.median(rows)))

        left_count = sum(x < edge_width for x in edge_x_valid)
        right_count = sum(x >= xPixelLen - edge_width for x in edge_x_valid)

        # Require usable points from both ends before extrapolating across the image.
        if left_count >= 2 and right_count >= 2 and len(set(edge_x_valid)) >= 4:
            center_x = (xPixelLen - 1) / 2
            scale_x = max(center_x, 1.0)
            normalized_x = (np.asarray(edge_x_valid) - center_x) / scale_x
            design = np.column_stack((normalized_x ** 2, normalized_x, np.ones_like(normalized_x)))
            a, b, c = np.linalg.lstsq(design, np.asarray(edge_y), rcond=None)[0]

            if abs(a) > 1e-8:
                vertex_normalized_x = -b / (2 * a)
                vertex_x = center_x + scale_x * vertex_normalized_x
                vertex_y = c - (b * b) / (4 * a)
                residuals = np.asarray(edge_y) - design @ np.array([a, b, c])
                fit_rmse = float(np.sqrt(np.mean(residuals ** 2)))

                # Do not apply a curve whose inferred vertex is outside the image
                # or whose endpoint samples do not agree with a quadratic.
                if (
                    0 <= vertex_x < xPixelLen
                    and 0 <= vertex_y < yPixelLen
                    and fit_rmse <= max(3.0, yPixelLen * 0.05)
                ):
                    all_x = np.arange(xPixelLen)
                    all_normalized_x = (all_x - center_x) / scale_x
                    curve_y = a * all_normalized_x ** 2 + b * all_normalized_x + c
                    curve_rows = np.rint(curve_y).astype(int)

                    # Preserve the original removal operation: invert a 6-pixel
                    # band along the completed curve, clipped to image bounds.
                    for x, row in enumerate(curve_rows):
                        top = max(0, row - 3)
                        bottom = min(yPixelLen, row + 3)
                        if top < bottom:
                            newImg[top:bottom, x] = 255 - newImg[top:bottom, x]

    if SAVE_PREPROCESS_DEBUG_IMAGE:
        source_path = Path(filePath)
        processed_path = source_path.with_name(f"{source_path.stem}_processed.png")
        if not cv2.imwrite(str(processed_path), newImg):
            raise OSError(f"無法儲存前處理圖片：{processed_path}")

    return newImg

def captchaOCR(filePath):
    processed_image = preprocess(filePath)
    result = OCR_ENGINE(processed_image)
    raw_text = "".join(result.txts or ())
    text = re.sub(r"[^A-Za-z0-9]", "", raw_text)

    if len(text) != 4:
        print(f"無法辨識（OCR 原始結果：{raw_text!r}；清理後：{text!r}）")
        return None

    return text
