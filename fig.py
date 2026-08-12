import matplotlib.pyplot as plt
import platform

# --- 1. 解決字體跑不出來的問題 ---
# 根據不同作業系統，自動設定對應的內建中文字體
system = platform.system()
if system == 'Darwin':  # macOS
    plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS']
elif system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
else:   # Linux
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC', 'WenQuanYi Micro Hei']

# 解決 y 軸負號顯示變成方塊的問題
plt.rcParams['axes.unicode_minus'] = False 

# --- 2. 資料定義 ---
age_groups = ['7-12歲', '13-15歲', '16-18歲', '19-44歲', '45-64歲', '65-74歲', '75歲以上']
male_prevalence = [0.0, 0.3, 1.1, 4.0, 15.6, 23.9, 27.8]
female_prevalence = [0.0, 0.2, 0.4, 1.6, 9.9, 23.1, 31.4]

# 建立畫布
plt.figure(figsize=(10, 6))

# 繪製折線圖
plt.plot(age_groups, male_prevalence, marker='o', color='#1f77b4', label='男性', linewidth=2.5, markersize=8)
plt.plot(age_groups, female_prevalence, marker='o', color='#d62728', label='女性', linewidth=2.5, markersize=8)

# 標籤與標題設定
plt.title('民國 106-109 年各年齡層糖尿病盛行率比較 (男性 vs 女性)', fontsize=16, pad=15)
plt.xlabel('年齡層', fontsize=12)
plt.ylabel('糖尿病盛行率 (%)', fontsize=12)

# --- 3. 解決數字標籤與圖標重疊的問題 ---
# 改用 annotate 的 xytext 來設定「相對像素位移」，確保數字與點保持固定距離
for i in range(len(age_groups)):
    # 男性數值標籤 (設定在點的上方 10 像素處)
    plt.annotate(f"{male_prevalence[i]}%", 
                 (i, male_prevalence[i]), 
                 textcoords="offset points", 
                 xytext=(0, 10), 
                 ha='center', color='#1f77b4', fontsize=10, fontweight='bold')
    
    # 女性數值標籤 (設定在點的下方 15 像素處)
    plt.annotate(f"{female_prevalence[i]}%", 
                 (i, female_prevalence[i]), 
                 textcoords="offset points", 
                 xytext=(0, -15), 
                 ha='center', color='#d62728', fontsize=10, fontweight='bold')

# 版面微調
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.legend(fontsize=12, loc='upper left')

# 將 Y 軸範圍稍微加大，避免最頂端或最底部的字被裁切
plt.ylim(-3, 36) 
plt.tight_layout()

# 顯示圖表
plt.show()