from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import os

app = FastAPI(title="我的自動化分類題庫系統")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 設定資料夾路徑
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def get_file_data(filename):
    """讀取單一 CSV 檔案"""
    filepath = os.path.join(DATA_DIR, filename)
    questions = []
    if not os.path.exists(filepath):
        return questions
    
    with open(filepath, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["id"] = int(row["id"])
            row["filename"] = filename # 標記檔案來源
            questions.append(row)
    return questions

@app.get("/api/categories")
def get_categories():
    """掃描資料夾，自動產出年份與分類清單"""
    years = set()
    categories = set()
    for f in os.listdir(DATA_DIR):
        if f.endswith(".csv"):
            # 檔名格式: 113_Micro.csv
            parts = f.replace(".csv", "").split('_')
            if len(parts) >= 2:
                years.add(parts[0])
                categories.add(parts[1])
    return {"years": sorted(list(years), reverse=True), "categories": sorted(list(categories))}

@app.get("/api/questions")
async def get_questions(year: str, category: str):
    """根據選定的年份與分類讀取檔案"""
    filename = f"{year}_{category}.csv"
    questions = get_file_data(filename)
    
    # 回傳篩選過後的必要欄位
    return [{
        "id": q["id"], "question": q["question"],
        "option_a": q["option_a"], "option_b": q["option_b"],
        "option_c": q["option_c"], "option_d": q["option_d"],
        "category": category
    } for q in questions]

@app.post("/api/submit")
def submit_answer(question_id: int, user_choice: str, year: str, category: str):
    """批改題目 (需要知道年份與分類才能找到對應檔案)"""
    questions = get_file_data(f"{year}_{category}.csv")
    q = next((item for item in questions if item["id"] == question_id), None)
    
    if not q:
        raise HTTPException(status_code=404, detail="找不到題目")
        
    return {
        "is_correct": (user_choice.upper() == q["correct_answer"].strip().upper()),
        "correct_answer": q["correct_answer"],
        "explanation": q["explanation"]
    }