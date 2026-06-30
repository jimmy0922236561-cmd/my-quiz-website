import os
import re
import csv
import pdfplumber

# 設定檔案路徑
PDF_PATH = os.path.join(os.path.dirname(__file__), "BM113_Block6_期末考詳解.pdf.pdf")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "questions.csv")

def parse_pdf_to_csv():
    if not os.path.exists(PDF_PATH):
        print(f"❌ 找不到 PDF 檔案，請確認檔案是否放在：{PDF_PATH}")
        return

    print("🚀 [第 3 版架構啟動] 開始精準匹配數字開頭題目...")
    parsed_questions = []
    
    current_id = None
    current_question = ""
    current_options = {"A": "", "B": "", "C": "", "D": ""}
    current_answer = ""
    current_explanation = ""
    current_category = "未分類"
    
    state = None 

    with pdfplumber.open(PDF_PATH) as pdf:
        for page_num, page in enumerate(pdf.pages[1:], start=2):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 1. 關鍵突破：匹配「數字開頭 + 空格」或「數字開頭 + 中文」
                # 例如 "1 下列何者錯誤？" -> 抓出 id=1, 剩餘字串當作題目起頭
                match_new_q = re.match(r"^(\d+)\s+(.*)$", line)
                
                if match_new_q:
                    q_id = int(match_new_q.group(1))
                    q_content = match_new_q.group(2)
                    
                    # 排除像 "2 6" (頁碼雜訊) 或者是出處裡面帶數字的情況
                    # 真正的題目通常會比較長，或者包含「何者」、「下列」或問號
                    if len(line) < 10 and not any(k in line for k in ["何者", "錯誤", "正確", "敘述"]):
                        # 這可能是頁碼（如 脂質代謝疾病 ⽩哲聲 2 6 拆出來的 6），當作一般文字處理
                        pass
                    else:
                        # 這是真正的下一題開始，存入上一題
                        if current_id is not None:
                            parsed_questions.append({
                                "id": current_id,
                                "question": current_question.strip(),
                                "option_a": current_options["A"].strip(),
                                "option_b": current_options["B"].strip(),
                                "option_c": current_options["C"].strip(),
                                "option_d": current_options["D"].strip(),
                                "correct_answer": current_answer.strip().upper(),
                                "explanation": current_explanation.strip(),
                                "category": current_category.strip()
                            })
                        
                        current_id = q_id
                        current_question = q_content + " "
                        current_options = {"A": "", "B": "", "C": "", "D": ""}
                        current_answer = ""
                        current_explanation = ""
                        current_category = "未分類"
                        state = "QUESTION"
                        continue
                
                # 2. 狀態切換關鍵字
                if line.startswith("答案"):
                    state = "ANSWER"
                    ans_match = re.search(r"\(([A-D])\)", line)
                    if ans_match:
                        current_answer = ans_match.group(1)
                    continue
                elif line.startswith("詳解"):
                    state = "EXPLANATION"
                    current_explanation += line.replace("詳解", "").strip() + " \\n "
                    continue
                elif line.startswith("出處"):
                    state = "SOURCE"
                    current_category = line.replace("出處", "").strip()
                    continue
                
                # 3. 根據狀態塞入內容
                if state == "QUESTION":
                    # 檢查這行是否包含選項 (A) ... (B) ...
                    opt_matches = re.findall(r"\(([A-D])\)\s*([^()]+)", line)
                    if opt_matches:
                        for opt, content in opt_matches:
                            current_options[opt] += content.strip() + " "
                    else:
                        # 排除頁碼與人名雜訊
                        if not ("⽩哲聲" in line or "Block" in line or "期末考詳解" in line):
                            current_question += line + " "
                        
                elif state == "ANSWER" and not current_answer:
                    ans_match = re.search(r"\(([A-D])\)", line)
                    if ans_match:
                        current_answer = ans_match.group(1)
                        
                elif state == "EXPLANATION":
                    current_explanation += line + " \\n "

        # 投遞最後一題
        if current_id is not None:
            parsed_questions.append({
                "id": current_id,
                "question": current_question.strip(),
                "option_a": current_options["A"].strip(),
                "option_b": current_options["B"].strip(),
                "option_c": current_options["C"].strip(),
                "option_d": current_options["D"].strip(),
                "correct_answer": current_answer.strip().upper(),
                "explanation": current_explanation.strip(),
                "category": current_category.strip()
            })

    # 4. 寫入 questions.csv
    headers = ["id", "question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation", "category"]
    
    with open(OUTPUT_CSV, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(parsed_questions)
        
    print(f"🎉 辨識完成！成功自動上架 {len(parsed_questions)} 題到 questions.csv 檔中！")

if __name__ == "__main__":
    parse_pdf_to_csv()