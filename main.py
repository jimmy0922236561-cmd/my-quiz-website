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
    questions_list = []
    if not os.path.exists(CSV_FILE_PATH):
        return questions_list

    with open(CSV_FILE_PATH, mode="r", encoding="utf-8-sig") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            questions_list.append({
                "id": int(row["id"]),
                "question": row["question"],
                "option_a": row["option_a"],
                "option_b": row["option_b"],
                "option_c": row["option_c"],
                "option_d": row["option_d"],
                "correct_answer": row["correct_answer"].strip().upper(),
                "explanation": row["explanation"],
                "category": row.get("category", "未分類")  # 讀取分類欄位，若沒有則填未分類
            })
    return questions_list


@app.get("/")
def home():
    return {"message": "分類題庫 API 伺服器正在運作中！"}


# 升級：允許前端傳入 category 參數來篩選題目（例如：/api/questions?category=解剖學）
@app.get("/api/questions")
def get_all_questions(category: str = None):
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
