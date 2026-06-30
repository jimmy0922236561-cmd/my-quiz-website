from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import os

app = FastAPI(title="我的獨立考卷分類題庫網站 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 💡 核心修改：動態讀取指定檔名的 CSV（預設放在 quizzes 資料夾內）
def read_questions_from_specific_csv(quiz_name: str):
    questions_list = []
    
    # 動態拼接路徑：專案根目錄/quizzes/考卷名稱.csv
    csv_path = os.path.join(os.path.dirname(__file__), "quizzes", f"{quiz_name}.csv")
    
    # 為了兼容你原本可能還沒建資料夾、放在根目錄的狀況，做一個雙重保險檢查
    if not os.path.exists(csv_path):
        # 備用路徑：嘗試直接在根目錄找 考卷名稱.csv
        csv_path = os.path.join(os.path.dirname(__file__), f"{quiz_name}.csv")
        
    if not os.path.exists(csv_path):
        print(f"❌ 找不到該份考卷的題庫檔案：{quiz_name}.csv")
        return None  # 回傳 None 讓外部路由丟出 404 錯誤

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # 防呆：如果那一行的 id 是空的，直接跳過，防止 int() 轉型崩潰
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
                print(f"⚠️ 解析第 {row.get('id')} 題時發生錯誤，已跳過。原因: {e}")
                continue
                
    return questions_list


@app.get("/")
def home():
    return {"message": "分頁與獨立考卷題庫 API 伺服器正在運作中！"}


# 🚀 1. 獲取特定考卷的題目（支援依科目分類篩選）
# 範例網址：/api/questions/Block7_Mid?category=消化系統免疫學 林明宏
@app.get("/api/questions/{quiz_name}")
async def get_questions(quiz_name: str, category: str = None):
    db_questions = read_questions_from_specific_csv(quiz_name)
    
    if db_questions is None:
        raise HTTPException(status_code=404, detail=f"找不到名為 '{quiz_name}' 的考卷檔案")
    
    safe_questions = []
    for q in db_questions:
        # 如果有指定科目，且這題的科目不符合，就跳過
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


# 🚀 2. 獲取特定考卷裡「目前所有的科目分類清單」（讓網頁知道這份考卷有哪些按鈕可以按）
# 範例網址：/api/categories/Block7_Mid
@app.get("/api/categories/{quiz_name}")
def get_categories(quiz_name: str):
    db_questions = read_questions_from_specific_csv(quiz_name)
    
    if db_questions is None:
        raise HTTPException(status_code=404, detail=f"找不到名為 '{quiz_name}' 的考卷檔案")
        
    categories = set([q["category"] for q in db_questions if q.get("category")])
    return list(categories)


# 🚀 3. 送出答案並判定（需要同時指定是哪份考卷以及哪一題）
# 範例網址：/api/submit/Block7_Mid
@app.post("/api/submit/{quiz_name}")
def submit_answer(quiz_name: str, question_id: int, user_choice: str):
    db_questions = read_questions_from_specific_csv(quiz_name)
    
    if db_questions is None:
        raise HTTPException(status_code=404, detail=f"找不到名為 '{quiz_name}' 的考卷檔案")
        
    target_question = None
    for q in db_questions:
        if q["id"] == question_id:
            target_question = q
            break
            
    if not target_question:
        raise HTTPException(status_code=404, detail="在此考卷中找不到該題號之題目")
        
    is_correct = (user_choice.upper() == target_question["correct_answer"])
    
    return {
        "quiz_name": quiz_name,
        "question_id": question_id,
        "your_answer": user_choice.upper(),
        "is_correct": is_correct,
        "correct_answer": target_question["correct_answer"],
        "explanation": target_question["explanation"]
    }