from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import os

app = FastAPI(title="我的分類題庫網站 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "questions.csv")

def read_questions_from_csv():
    import csv
    import os
    
    questions_list = []
    # 請確保 questions.csv 的路徑符合你專案的結構
    csv_path = os.path.join(os.path.dirname(__file__), "questions.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ 找不到題庫檔案：{csv_path}")
        return questions_list

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        # 💡 在這裡正式定義了 reader！
        reader = csv.DictReader(f)
        
        for row in reader:
            # 💡 核心防呆：如果那一行的 id 是空的，直接跳過，防止 int() 轉型崩潰
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
                    "category": row.get("category", "未分類").strip()
                }
                questions_list.append(q_data)
            except Exception as e:
                print(f"⚠️ 解析第 {row.get('id')} 題時發生錯誤，跳過該題。錯誤原因: {e}")
                continue
                
    return questions_list


@app.get("/")
def home():
    return {"message": "分類題庫 API 伺服器正在運作中！"}


# 升級：允許前端傳入 category 參數來篩選題目（例如：/api/questions?category=解剖學）
@app.get("/api/questions")
async def get_questions(year: str = None, category: str = None):
    db_questions = read_questions_from_csv()
    
    safe_questions = []
    for q in db_questions:
        # 如果有指定分類，且這題的分類跟指定的不一樣，就跳過它
        if category and q["category"] != category:
            continue
            
        safe_questions.append({
            "id": q["id"],
            "question": q["question"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "category": q["category"]
        })
    return safe_questions


# 獲取目前所有的分類清單（讓網頁知道有哪些科目可以選）
@app.get("/api/categories")
def get_categories():
    db_questions = read_questions_from_csv()
    categories = set([q["category"] for q in db_questions]) # 取得所有不重複的分類
    return list(categories)


@app.post("/api/submit")
def submit_answer(question_id: int, user_choice: str):
    db_questions = read_questions_from_csv()
    target_question = None
    for q in db_questions:
        if q["id"] == question_id:
            target_question = q
            break
            
    if not target_question:
        raise HTTPException(status_code=404, detail="找不到該題目")
        
    is_correct = (user_choice.upper() == target_question["correct_answer"])
    
    return {
        "question_id": question_id,
        "your_answer": user_choice.upper(),
        "is_correct": is_correct,
        "correct_answer": target_question["correct_answer"],
        "explanation": target_question["explanation"]
    }
