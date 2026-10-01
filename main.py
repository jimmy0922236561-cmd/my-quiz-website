from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import csv
import os
import glob
from openai import OpenAI

app = FastAPI(title="醫學系 Block / 國考 分類題庫 API")

# 設定 CORS 跨域請求（確保 GitHub Pages 前端能正常呼叫）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# 🤖 OpenAI (ChatGPT) 初始化與資料模型
# -------------------------------------------------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
# 初始化 OpenAI Client（若有設定環境變數則自動帶入）
openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

class AIChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None  # 接收前端傳來的自訂 System Prompt

class ExplanationUpdate(BaseModel):
    question_id: int
    explanation: str

# -------------------------------------------------------------
# 工具函式：檔案路徑與年份標籤解析
# -------------------------------------------------------------
def get_quizzes_dir():
    """動態取得 quizzes 資料夾路徑"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    quizzes_dir = os.path.join(base_dir, "quizzes")
    if os.path.exists(quizzes_dir):
        return quizzes_dir
    return base_dir

def parse_year_label(quiz_name: str) -> str:
    """將檔名 (如 Block7_113_Mid) 轉為易讀年份標籤 (113年 期中考)"""
    if not quiz_name:
        return ""
    parts = quiz_name.split("_")
    if len(parts) >= 3:
        year = parts[1]
        exam_type = parts[2]
        exam_map = {
            "Mid": "期中考",
            "Final": "期末考",
            "Fir": "第一次國考",
            "Sec": "第二次國考"
        }
        return f"{year}年 {exam_map.get(exam_type, exam_type)}"
    return quiz_name

def read_questions_from_specific_csv(quiz_name: str):
    """讀取單一 CSV 檔案"""
    quizzes_dir = get_quizzes_dir()
    csv_path = os.path.join(quizzes_dir, f"{quiz_name}.csv")
    if not os.path.exists(csv_path):
        return None

    questions_list = []
    year_label = parse_year_label(quiz_name)

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id") or str(row["id"]).strip() == "":
                continue
            try:
                # 兼容 correct_answer / answer / ans
                correct = row.get("correct_answer") or row.get("answer") or row.get("ans") or ""
                
                q_data = {
                    "id": row["id"].strip(),
                    "question": row.get("question", ""),
                    "option_a": row.get("option_a", ""),
                    "option_b": row.get("option_b", ""),
                    "option_c": row.get("option_c", ""),
                    "option_d": row.get("option_d", ""),
                    "correct_answer": correct.strip().upper(),
                    "explanation": row.get("explanation", ""),
                    "category": (row.get("category") or "未分類").strip(),
                    "teacher": (row.get("teacher") or "").strip(),
                    "year_label": year_label,
                    "ai_explanation": (row.get("ai_explanation") or "").strip(),
                    "image_url": (row.get("image_url") or "").strip()
                }
                questions_list.append(q_data)
            except Exception:
                continue
    return questions_list

def write_questions_to_csv(quiz_name: str, questions_list: list):
    """寫回筆記到 CSV，確保完整保留所有欄位"""
    quizzes_dir = get_quizzes_dir()
    csv_path = os.path.join(quizzes_dir, f"{quiz_name}.csv")
        
    fieldnames = [
        "id", "question", "option_a", "option_b", "option_c", "option_d",
        "correct_answer", "explanation", "category", "teacher", "ai_explanation", "image_url"
    ]
    
    with open(csv_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for q in questions_list:
            writer.writerow({
                "id": q.get("id", ""),
                "question": q.get("question", ""),
                "option_a": q.get("option_a", ""),
                "option_b": q.get("option_b", ""),
                "option_c": q.get("option_c", ""),
                "option_d": q.get("option_d", ""),
                "correct_answer": q.get("correct_answer", ""),
                "explanation": q.get("explanation", ""),
                "category": q.get("category", "未分類"),
                "teacher": q.get("teacher", ""),
                "ai_explanation": q.get("ai_explanation", ""),
                "image_url": q.get("image_url", "")
            })

# -------------------------------------------------------------
# 基礎狀態確認
# -------------------------------------------------------------
@app.get("/")
def home():
    return {"message": "醫學系考古題庫 API 伺服器正常運作中！"}

# -------------------------------------------------------------
# 🤖 0. AI 助教對話 API (GPT-4o-mini)
# -------------------------------------------------------------
@app.post("/api/ai_chat")
async def ai_chat(req: AIChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="問題內容不能為空")

    if not openai_client:
        raise HTTPException(status_code=500, detail="後端尚未設定 OPENAI_API_KEY 環境變數")

    try:
        # 若前端有傳入自訂 Prompt 就使用自訂，否則使用預設醫學導師角色
        system_instruction = req.system_prompt or (
            "你是一位頂尖的醫學教授與國考輔導主治醫師，負責為醫學生解答考古題。"
            "請以邏輯清晰、醫學機轉嚴謹的繁體中文回答，指出各選項對錯的核心機轉與臨床盲點。"
        )

        # 呼叫 GPT-4o-mini
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": req.message}
            ],
            temperature=0.3  # 降低隨機度，使生理、病理、藥理等醫學機轉推論更穩定精準
        )

        reply_text = completion.choices[0].message.content
        return {"reply": reply_text}

    except Exception as e:
        print(f"OpenAI API 錯誤: {e}")
        return {"reply": f"AI 助教連線異常：{str(e)}"}

# -------------------------------------------------------------
# 1. 單一考卷 API
# -------------------------------------------------------------
@app.get("/api/questions/{quiz_name}")
async def get_questions(quiz_name: str, category: str = None):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
    
    if category:
        return [q for q in db_questions if q["category"] == category]
    return db_questions

@app.get("/api/categories/{quiz_name}")
def get_categories(quiz_name: str):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
    
    categories = list(dict.fromkeys(
        q["category"] for q in db_questions if q.get("category") and q["category"] != "未分類"
    ))
    return categories

# -------------------------------------------------------------
# 2. 跨年度專題特訓 API
# -------------------------------------------------------------
@app.get("/api/block_categories/{block_name}")
def get_block_categories(block_name: str):
    """跨年度：取得指定 Block 在所有年份中出現過的不重複科目清單"""
    quizzes_dir = get_quizzes_dir()
    pattern = os.path.join(quizzes_dir, f"{block_name}_*.csv")
    csv_files = glob.glob(pattern)

    if not csv_files:
        return []

    categories = set()
    for file_path in csv_files:
        filename = os.path.basename(file_path).replace(".csv", "")
        questions = read_questions_from_specific_csv(filename)
        if questions:
            for q in questions:
                cat = q.get("category")
                if cat and cat != "未分類":
                    categories.add(cat)

    return sorted(list(categories))

@app.get("/api/block_questions/{block_name}")
def get_block_questions(block_name: str, category: str = None):
    """跨年度：彙整指定 Block 所有年份考卷的題目（支援單一科目篩選）"""
    quizzes_dir = get_quizzes_dir()
    pattern = os.path.join(quizzes_dir, f"{block_name}_*.csv")
    csv_files = sorted(glob.glob(pattern), reverse=True)  # 年份由新到舊

    if not csv_files:
        return []

    all_questions = []
    for file_path in csv_files:
        filename = os.path.basename(file_path).replace(".csv", "")
        questions = read_questions_from_specific_csv(filename)
        if not questions:
            continue

        for q in questions:
            if category and q.get("category") != category:
                continue
            
            # 跨卷合成唯一 ID，避免第 1 題題號衝突
            q_copy = dict(q)
            q_copy["id"] = f"{filename}_{q['id']}"
            all_questions.append(q_copy)

    return all_questions

# -------------------------------------------------------------
# 3. 提交與筆記更新
# -------------------------------------------------------------
@app.post("/api/explanation/{quiz_name}")
def update_question_explanation(quiz_name: str, data: ExplanationUpdate):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
        
    found = False
    for q in db_questions:
        if str(q["id"]) == str(data.question_id):
            q["explanation"] = data.explanation 
            found = True
            break
            
    if not found:
        raise HTTPException(status_code=404, detail="找不到對應題目")
        
    write_questions_to_csv(quiz_name, db_questions)
    return {"status": "success", "message": "筆記已寫入 CSV！"}