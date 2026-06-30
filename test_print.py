import os
import pdfplumber

PDF_PATH = os.path.join(os.path.dirname(__file__), "BM113_Block6_期末考詳解.pdf.pdf")

if os.path.exists(PDF_PATH):
    with pdfplumber.open(PDF_PATH) as pdf:
        # 只印出第 2 頁（索引 1）的前 1000 個字來檢查結構
        print("--- 第 2 頁真實文字內容 ---")
        print(pdf.pages[1].extract_text()[:1000])
else:
    print("找不到 PDF 檔案")