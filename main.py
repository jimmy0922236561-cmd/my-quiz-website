from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import os

app = FastAPI(title="我的獨立考卷分類題庫網站 API (整合筆記與詳解)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 💡 定義前端傳過來的資料格式
class ExplanationUpdate(BaseModel):
    question_id: int
    explanation: str

def read_questions_from_specific_csv(quiz_name: str):
    questions_list = []
    csv_path = os.path.join(os.path.dirname(__file__), "quizzes", f"{quiz_name}.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), f"{quiz_name}.csv")
    if not os.path.exists(csv_path):
        return None

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id") or row["id"].strip() == "":
                continue
            try:
                q_data = {
                    "id": int(row["id"].strip()),
                    "question": row.get("question", ""),
                    "option_a": row.get("option_a", ""),
                    "option_b": row.get("option_b", ""),
                    "option_c": row.get("option_c", ""),
                    "option_d": row.get("option_d", ""),
                    "correct_answer": row.get("correct_answer", "").strip().upper(),
                    "explanation": row.get("explanation", ""),
                    "category": row.get("category", "未分類").strip(),
                    
                    # 🎯 核心修正 1：確保從 CSV 讀取時，有把 AI 詳解抓進記憶體！
                    "ai_explanation": row.get("ai_explanation", "").strip()
                }
                questions_list.append(q_data)
            except Exception as e:
                continue
    return questions_list

def write_questions_to_csv(quiz_name: str, questions_list: list):
    csv_path = os.path.join(os.path.dirname(__file__), "quizzes", f"{quiz_name}.csv")
    if not os.path.exists(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), f"{quiz_name}.csv")
        
    # 🎯 核心修正 2：在欄位清單最後面補上 "ai_explanation"。
    # 這樣同學儲存手寫筆記時，AI 欄位才不會被當成垃圾蒸發掉，而是會安全地一起存回去！
    fieldnames = ["id", "question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation", "category", "ai_explanation"]
    
    with open(csv_path, mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for q in questions_list:
            # 防禦性確保每一題都有這個 key
            if "ai_explanation" not in q:
                q["ai_explanation"] = ""
            writer.writerow(q)

@app.get("/")
def home():
    return {"message": "整合詳解筆記 API 伺服器運作中！"}

@app.get("/api/questions/{quiz_name}")
async def get_questions(quiz_name: str, category: str = None):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
    
    safe_questions = []
    for q in db_questions:
        if category and q["category"] != category:
            continue
        safe_questions.append({
            "id": q["id"],
            "question": q["question"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "category": q["category"],
            "explanation": q.get("explanation", ""),
            
            # 🎯 核心修正 3：此時記憶體裡有資料了，順利放行傳給前端網頁
            "ai_explanation": q.get("ai_explanation", "")
        })
    return safe_questions

@app.post("/api/submit/{quiz_name}")
def submit_answer(quiz_name: str, question_id: int, user_choice: str):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
    target_question = None
    for q in db_questions:
        if q["id"] == question_id:
            target_question = q
            break
    if not target_question:
        raise HTTPException(status_code=404, detail="找不到該題目")
        
    return {
        "quiz_name": quiz_name,
        "question_id": question_id,
        "your_answer": user_choice.upper(),
        "is_correct": (user_choice.upper() == target_question["correct_answer"]),
        "correct_answer": target_question["correct_answer"],
        "explanation": target_question["explanation"] 
    }

# 直接更新並複寫某題 explanation 的 API
@app.post("/api/explanation/{quiz_name}")
def update_question_explanation(quiz_name: str, data: ExplanationUpdate):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
        
    found = False
    for q in db_questions:
        if q["id"] == data.question_id:
            q["explanation"] = data.explanation 
            found = True
            break
            
    if not found:
        raise HTTPException(status_code=404, detail="找不到對應題目")
        
    write_questions_to_csv(quiz_name, db_questions)
    return {"status": "success", "message": "筆記/詳解已更新並寫入 CSV！"}

@app.get("/api/categories/{quiz_name}")
def get_categories(quiz_name: str):
    db_questions = read_questions_from_specific_csv(quiz_name)
    if db_questions is None:
        raise HTTPException(status_code=404, detail="找不到考卷")
    categories = set([q["category"] for q in db_questions if q.get("category")])
    return list(categories)