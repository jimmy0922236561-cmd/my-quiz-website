import csv
import os

# 這裡內含了 BM113 Block 6 所有的題目資料，最後一欄已改為老師出處
ALL_QUESTIONS_DATA = [
    {
        "id": 1,
        "question": "下列何者錯誤？",
        "option_a": "(A)丙二醯輔酶A(Malonyl CoA)會抑制CPT1,減少脂肪酸的氧化",
        "option_b": "(B)丙二醯輔酶A(Malonyl CoA)可以透過脂肪酸合成酶(Fatty acid synthase) 合成脂肪酸",
        "option_c": "(C)棕櫚酸(Palmitic acid)是一種必須脂肪酸,人體無法自行合成",
        "option_d": "(D)人體在饑餓的狀況下,會產生酮體(ketone body)作為能量來源",
        "correct_answer": "C",
        "explanation": "必需脂肪酸大多為omega-6和omega-3的脂肪酸。棕櫚酸人體可以合成，是非必需脂肪酸。",
        "category": "脂質代謝疾病 白哲聲"
    },
    {
        "id": 2,
        "question": "下列敘述何者錯誤？",
        "option_a": "(A)低密度脂蛋白受體(LDL receptor)發生突變失去功能,會減少血中低密度脂蛋白膽固醇,加速動脈粥狀硬化",
        "option_b": "(B) Ezetimibe 可以抑制腸道中膽固醇的吸收硬化",
        "option_c": "(C)降膽固醇首選藥物是 statin 類",
        "option_d": "(D) fibrate 透過刺激過氧化物酶體增殖物活化受體a (PPAR a receptor)來降低血中三酸甘油脂(Triglyceride)",
        "correct_answer": "A",
        "explanation": "LDL受體功能喪失會增加血中LDL膽固醇，並加速動脈粥狀硬化及相關的心血管疾病。",
        "category": "脂質代謝疾病 白哲聲"
    },
    {
        "id": 3,
        "question": "下列何者正確？",
        "option_a": "(A)逆向膽固醇運輸(Reverse cholesterol transport)中,最重要的脂蛋白(lipoprotein)是LDL",
        "option_b": "(B) Chylomicron remant 透過其上的載脂蛋白E(ApoE)結合肝臟的受體回收到肝臟",
        "option_c": "(C) Chylomicron 負責空腹時的三酸甘油脂(Triglyceride)運輸",
        "option_d": "(D)肝臟產生載脂蛋白B48(ApoB48)來構成 VLDL",
        "correct_answer": "B",
        "explanation": "(A)逆向膽固醇運輸的主要脂蛋白是HDL。(C)Chylomicron主要在餐後運輸飲食中的三酸甘油酯，空腹時由VLDL運輸。(D)ApoB48由小腸合成，肝臟合成的是ApoB100。",
        "category": "脂質代謝疾病 白哲聲"
    },
    {
        "id": 4,
        "question": "下列何者是 lipoprotein lipase (LPL)的主要作用？",
        "option_a": "(A)促進膽固醇合成",
        "option_b": "(B)促進三酸甘油脂水解",
        "option_c": "(C)促進葡萄糖吸收",
        "option_d": "(D)促進肝臟葡萄糖生成",
        "correct_answer": "B",
        "explanation": "LPL的功能：促進三酸甘油酯的水解和製造HDL。",
        "category": "脂質代謝疾病 白哲聲"
    },
    {
        "id": 5,
        "question": "關於高血脂疾病的敘述何者錯誤？",
        "option_a": "(A) Dysbetalipoproteinemia 的成因是因為 Apolipoprotein E有突變,造成脂蛋白回收異常",
        "option_b": "(B) Familial Hypercholesterolemia的患者,總膽固醇一定會超過900mg/dL",
        "option_c": "(C)糖尿病會造成的血脂異常為三酸甘油脂上升,HDL 下降",
        "option_d": "(D)肝臟的 Apolipoprotein B 製造增加,一般會讓血中三酸甘油脂及LDL 上升",
        "correct_answer": "B",
        "explanation": "Heterozygous形式總膽固醇>300mg/dL；Homozygous形式總膽固醇>600mg/dL(600-1000 mg/dl)，並非一定超過900。",
        "category": "脂質代謝疾病 白哲聲"
    },
    {
        "id": 6,
        "question": "下列何者錯誤？",
        "option_a": "(A) statin類藥物是一種抑制 HMG-CoA還原酶的藥物,可以增加膽固醇的合成",
        "option_b": "(B)雌激素 Estrogen 會降低LDL 的濃度",
        "option_c": "(C)甲狀腺低下的患者其血中膽固醇濃度可能會上升",
        "option_d": "(D)高三酸甘油脂血症會增加胰臟炎的風險",
        "correct_answer": "A",
        "explanation": "敘述(A)中的「可以增加膽固醇的合成」是不正確的，因為statin的作用是降低膽固醇合成。",
        "category": "脂質代謝疾病 白哲聲"
    },
    {
        "id": 7,
        "question": "腎上腺皮質分泌哪一類激素？",
        "option_a": "(A)糖皮質激素、鹽皮質激素、性激素",
        "option_b": "(B)兒茶酚胺(Catecholamines)",
        "option_c": "(C)甲狀腺素(Thyroxine, T4)",
        "option_d": "(D)胰島素(Insulin)",
        "correct_answer": "A",
        "explanation": "腎上腺皮質激素(Adrenocortical hormones)包含：鹽皮質激素、糖皮質激素、雄性素。",
        "category": "腎上腺生理學 鄭琮霖"
    },
    {
        "id": 8,
        "question": "腎上腺髓質分泌的主要激素是？",
        "option_a": "(A)皮質醇(Cortisol)",
        "option_b": "(B)醛固酮(Aldosterone)",
        "option_c": "(C)腎上腺素與正腎上腺素",
        "option_d": "(D)甲狀腺素",
        "correct_answer": "C",
        "explanation": "腎上腺髓質經下視丘的神經刺激後會釋放腎上腺素與正腎上腺素。",
        "category": "腎上腺生理學 鄭琮霖"
    },
    {
        "id": 9,
        "question": "皮質醇(Cortisol)的主要作用是？",
        "option_a": "(A)降低血糖",
        "option_b": "(B)抑制免疫反應並促進糖質新生作用",
        "option_c": "(C)促進水分重吸收",
        "option_d": "(D)直接刺激肌肉收縮",
        "correct_answer": "B",
        "explanation": "Cortisol的主要作用包括於肝臟促進糖質新生作用(Gluconeogenesis)，並有抗發炎與抑制免疫反應的效果。",
        "category": "腎上腺生理學 鄭琮霖"
    },
    {
        "id": 10,
        "question": "當人體受到壓力(如受傷或飢餓)時,哪種激素的分泌會增加？",
        "option_a": "(A)甲狀腺素(T4)",
        "option_b": "(B)胰島素(Insulin)",
        "option_c": "(C)皮質醇(Cortisol)",
        "option_d": "(D)雌激素(Estrogen)",
        "correct_answer": "C",
        "explanation": "壓力會增加ACTH的分泌，進而導致糖皮質激素(Cortisol)釋放增加。",
        "category": "腎上腺生理學 鄭琮霖"
    },
    {
        "id": 11,
        "question": "促腎上腺皮質激素(ACTH) 對腎上腺的影響是？",
        "option_a": "(A)刺激腎上腺髓質分泌腎上腺素",
        "option_b": "(B)促進腎上腺髓質分泌正腎上腺素",
        "option_c": "(C)促進腎上腺皮質分泌醛固酮",
        "option_d": "(D)促進腎上腺皮質分泌皮質醇",
        "correct_answer": "D",
        "explanation": "HPA軸：下視丘(CRH) -> 腦下垂體前葉(ACTH) -> 腎上腺皮質(cortisol)。",
        "category": "腎上腺生理學 鄭琮霖"
    },
    {
        "id": 12,
        "question": "醛固酮(Aldosterone)的主要作用是？",
        "option_a": "(A)調節血鈣濃度",
        "option_b": "(B)促進鈉離子重吸收並排出鉀離子",
        "option_c": "(C)降低血壓",
        "option_d": "(D)促進胰島素分泌",
        "correct_answer": "B",
        "explanation": "Aldosterone的功能為促進腎小管重吸收鈉離子(Na+)，並分泌排出鉀離子(K+)或氫離子(H+)。",
        "category": "腎上腺生理學 鄭琮霖"
    },
    {
        "id": 13,
        "question": "甲狀腺激素(T3/T4)主要的生理功能是？",
        "option_a": "(A)促進骨骼生長與調節鈣平衡",
        "option_b": "(B)調節基礎代謝率與能量消耗",
        "option_c": "(C)促進腎上腺素的分泌",
        "option_d": "(D)促進血糖降低",
        "correct_answer": "B",
        "explanation": "甲狀腺激素的主要整體效應是增加氧氣消耗與提升基礎代謝率(Metabolic rate)。",
        "category": "甲狀腺的生理學 鄭琮霖"
    },
    {
        "id": 14,
        "question": "促進甲狀腺激素(T3/T4)分泌的主要調控激素是？",
        "option_a": "(A)促腎上腺皮質激素(ACTH)",
        "option_b": "(B)黃體生成激素(LH)",
        "option_c": "(C)促甲狀腺激素(TSH)",
        "option_d": "(D)抗利尿激素(ADH)",
        "correct_answer": "C",
        "explanation": "TSH由腦下垂體前葉分泌，作用是促進甲狀腺合成與釋放T3與T4。",
        "category": "甲狀腺的生理學 鄭琮霖"
    },
    {
        "id": 15,
        "question": "甲狀腺功能亢進(Hyperthyroidism)可能引起哪種症狀？",
        "option_a": "(A)體重增加、心跳變慢",
        "option_b": "(B)易疲倦、怕冷",
        "option_c": "(C)血糖降低、皮膚乾燥",
        "option_d": "(D)心跳加快、食慾增加、體重下降",
        "correct_answer": "D",
        "explanation": "甲狀腺功能亢進的特徵包括活動力增加、對熱耐受性差、多汗、心跳加快、食慾上升但體重下降。",
        "category": "甲狀腺的生理學 鄭琮霖"
    },
    {
        "id": 16,
        "question": "關於Hypercortisolism (Cushing syndrome)庫興氏症候群的敘述,下列何者為不正確？",
        "option_a": "(A)最常見造成Cushing syndrome的原因是屬於外因性(Exogenous)",
        "option_b": "(B)腎上腺腺瘤(Adrenal adenoma)造成的Cushing syndrome是屬於ACTH independent",
        "option_c": "(C)腦下垂體腺瘤(Pituitary adenoma)導致的Cushing syndrome是ACTH dependent",
        "option_d": "(D)肺小細胞肺癌(Small cell carcinoma)導致的Cushing syndrome是屬於ACTH independent",
        "correct_answer": "D",
        "explanation": "非腦下垂體腫瘤（如肺小細胞肺癌）分泌異位性ACTH造成的Cushing症候群，屬於ACTH dependent。",
        "category": "腎上腺病理學 簡竹君"
    },
    {
        "id": 17,
        "question": "下列關於Hyperaldosteronism (高醛固酮症)的描述,何者不正確？",
        "option_a": "(A)最常見的原因是醛固酮分泌腺瘤Aldosterone-producing adenoma",
        "option_b": "(B)醛固酮分泌腺瘤(Aldosterone-producing adenoma)顯微鏡下可見spironolactone bodies",
        "option_c": "(C)臨床最常見的症狀為高血壓(Hypertension)",
        "option_d": "(D)會因為低血鉀(Hypokalemia)而出現肌肉無力及感覺異常(paresthesia)",
        "correct_answer": "A",
        "explanation": "最常見的原因是Iatrogenic醫源性(給類固醇)，在排除外因後，有70%是由Cushing's disease(腦下垂體腺瘤)造成。",
        "category": "腎上腺疾病:庫欣氏症候群及腎上腺機能不足 李美月"
    },
    {
        "id": 18,
        "question": "關於腎上腺皮質機能低下症(Adrenocortical insufficiency)的敘述,以下何者不正確？",
        "option_a": "(A) Waterhouse-Friderichsen syndrome 和急性細菌感染有關",
        "option_b": "(B)造成 Addison disease 最常見的原因是 Autoimmune adrenalitis",
        "option_c": "(C)常見臨床表現為低血壓(Hypotension)和低血鉀(Hypokalemia)",
        "option_d": "(D)結核菌感染(Tuberculosis)是可能的原因",
        "correct_answer": "C",
        "explanation": "醛固酮分泌不足會導致高血鉀(Hyperkalemia)、低血鈉與低血壓，因此(C)錯誤。",
        "category": "腎上腺病理學 簡竹君"
    },
    {
        "id": 19,
        "question": "若發育出可與自身多價抗原產生強烈交聯作用的B細胞,下列何者較不可能是正常情況下其自我耐受性的形成過程？",
        "option_a": "(A)中央耐受性形成時,此種B細胞可能經過受器編輯,又再經過株落刪除",
        "option_b": "(B)在骨髓中,此種B細胞會優先進行受器編輯機制改造受器",
        "option_c": "(C)進入次級淋巴組織時,B細胞在次級免疫反應時為了達到受器的親和力成熟,進行體細胞高度突變,再次產生此種自體反應B細胞",
        "option_d": "(D)在次級淋巴組織如脾臟中,此種B細胞之免疫球蛋白輕鍊基因進行再次重組,合併之前的重鍊基因,表現新的受器",
        "correct_answer": "D",
        "explanation": "脾臟走周邊耐受性機制。因為周邊RAG基因已經關閉(turn off)，無法再重組，因此只能進行株落刪除(clonal deletion)與凋亡，無法進行受器編輯(Receptor editing)。",
        "category": "內分泌系統的自體免疫調節 陳怡菁"
    },
    {
        "id": 20,
        "question": "有關 FoxP3 基因的重要性及影響,下列敘述何者正確？",
        "option_a": "(A)此基因缺損或突變,極可能造成第一型自體免疫多腺症候群(APS-1)疾病的發生",
        "option_b": "(B)此基因缺損或突變,極可能造成IPEX症候群的發生",
        "option_c": "(C)此基因的表現,主要是影響之胸腺髓質細胞(mTEC)上的自體組織特異性抗原的表現",
        "option_d": "(D)此基因的表現,主要在直接影響效應T細胞(effector T cell)受到抗原呈現細胞的共同刺激效果",
        "correct_answer": "B",
        "explanation": "FOXP3基因主要影響CD4+CD25+調節性T細胞(Treg)的功能，缺陷對應到IPEX症候群。APS-1則是AIRE基因缺陷。",
        "category": "內分泌系統的自體免疫調節 陳怡菁"
    },
    {
        "id": 21,
        "question": "關於第一型糖尿病(type 1 diabetes mellitus)之發生,下列敘述何者正確？",
        "option_a": "(A)是一種全身性自體免疫疾病,將影響身上許多組織",
        "option_b": "(B) MHC class II 的HLA基因型表現 HLA-DR2者,較健康正常者易於得到此症",
        "option_c": "(C)患者能產生自體反應之B細胞及T細胞,免疫病理主要來自自體反應T細胞,自體反應B細胞則是作為抗原呈現細胞之用",
        "option_d": "(D)患者最主要的免疫病理機制是產生與自體胰島細胞抗原反應之抗體,影響胰島素的製造而致病",
        "correct_answer": "C",
        "explanation": "(A)第一型糖尿病屬於器官特異性自體免疫疾病。(B)HLA-DR2對第一型糖尿病具有保護作用(Protection)，DR3/DR4才是危險基因。(D)主要導致胰島細胞破壞的是CD8+ T細胞的毒殺作用，抗體多為伴隨產物。",
        "category": "內分泌系統的自體免疫調節 陳怡菁"
    },
    {
        "id": 22,
        "question": "一名BMI34的45歲男性,近期確診為第2型糖尿病,無心血管或腎臟疾病,最合適的第一線口服或注射藥物為？",
        "option_a": "(A) Metformin",
        "option_b": "(B) Insulin",
        "option_c": "(C) GLP-1 agonist",
        "option_d": "(D) Sulfonylurea",
        "correct_answer": "A",
        "explanation": "Metformin是第2型糖尿病合併肥胖、胰島素阻抗患者的典型第一線首選口服藥物。",
        "category": "口服降血糖藥 李美月"
    },
    {
        "id": 23,
        "question": "哪一類降血糖藥物在腎功能不全患者使用時需特別小心或調整劑量？",
        "option_a": "(A) Sulfonylureas",
        "option_b": "(B) DPP-4 抑制劑",
        "option_c": "(C) Metformin",
        "option_d": "(D)以上皆是",
        "correct_answer": "D",
        "explanation": "SU類在老人及腎功能不全易蓄積導致低血糖；DPP-4除了Linagliptin外皆需依腎功能調整；Metformin在eGFR<30時禁用。因此三者皆需小心或調整。",
        "category": "口服降血糖藥 李美月"
    },
    {
        "id": 24,
        "question": "下列哪一種口服降血糖藥物最容易造成低血糖？",
        "option_a": "(A) Metformin",
        "option_b": "(B) DPP-4 抑制劑",
        "option_c": "(C) SGLT2 抑制劑",
        "option_d": "(D) Sulfonylureas",
        "correct_answer": "D",
        "explanation": "磺醯脲類(Sulfonylureas, SU)因為促進胰島素分泌，是最容易且最嚴重造成低血糖的口服降血糖藥。",
        "category": "口服降血糖藥 李美月"
    },
    {
        "id": 25,
        "question": "下列關於胰島素在正常生理狀況下的功能,何者正確？",
        "option_a": "(A)促進肝臟糖質分解(glycogenolysis)",
        "option_b": "(B)抑制脂肪合成(lipogenesis)",
        "option_c": "(C)促進葡萄糖進入肌肉與脂肪細胞",
        "option_d": "(D)刺激升糖素(glucagon)分泌",
        "correct_answer": "C",
        "explanation": "胰島素能促進葡萄糖進入肌肉與脂肪細胞作為能量、促進脂肪與蛋白質合成、抑制糖原分解、並抑制升糖素分泌。",
        "category": "口服降血糖藥 李美月"
    },
    {
        "id": 26,
        "question": "病人接受基礎-餐時(basal-bolus) 胰島素治療,下列組合最合理？",
        "option_a": "(A) NPH + insulin lispro",
        "option_b": "(B) Insulin glargine + insulin aspart",
        "option_c": "(C) Insulin detemir + insulin regular",
        "option_d": "(D) Insulin glargine + insulin NPH",
        "correct_answer": "B",
        "explanation": "Basal-Bolus組合包含長效基礎型（如Glargine/Detemir）與餐前施打的速效型（如Aspart/Lispro）或短效型胰島素。",
        "category": "口服及注射降血糖藥Medications 李美月"
    },
    {
        "id": 27,
        "question": "65 歲男性,罹患第2型糖尿病10年,近來使用 basal-bolus regimen (insulin glargine + insulin lispro)。早上空腹血糖常高達 190 mg/dL,餐後血糖控制良好, HbA1c 7.8%。下列哪項調整最適合？",
        "option_a": "(A)增加晚餐後 lispro 劑量",
        "option_b": "(B)減少早餐前 lispro 劑量",
        "option_c": "(C)增加 insulin glargine 劑量",
        "option_d": "(D)改用 premixed insulin",
        "correct_answer": "C",
        "explanation": "速效(Lispro)控制餐後血糖，長效(Glargine)負責控制基礎空腹血糖。空腹血糖高代表基礎劑量不足，應調高長效胰島素劑量。",
        "category": "口服及注射降血糖藥Medications 李美月"
    },
    {
        "id": 28,
        "question": "ACTH 高且皮質醇低,ACTH 刺激測試反應不足,最可能診斷？",
        "option_a": "(A)中樞型腎上腺功能不全",
        "option_b": "(B)藥物造成的類固醇抑制",
        "option_c": "(C)原發性腎上腺功能不全",
        "option_d": "(D)假性低皮質醇血症",
        "correct_answer": "C",
        "explanation": "高ACTH伴隨皮質醇低下，且Cosyntropin刺激測試後反應低下(Subnormal)，代表病灶在腎上腺本身，屬於原發性腎上腺功能不全。",
        "category": "腎上腺疾病:庫欣氏症候群及腎上腺機能不足 李美月"
    },
    {
        "id": 29,
        "question": "下列哪一感染與 Addison disease 最相關？",
        "option_a": "(A)肺炎鏈球菌",
        "option_b": "(B)肝炎病毒",
        "option_c": "(C)結核菌感染",
        "option_d": "(D)巨細胞病毒",
        "correct_answer": "C",
        "explanation": "在慢性原發性腎上腺功能不全(Addison's disease)的感染病因中，結核菌(Tuberculosis)是最為經典且重要的病原體。",
        "category": "腎上腺疾病:庫欣氏症候群及腎上腺機能不足 李美月"
    },
    {
        "id": 30,
        "question": "慢性 adrenal insufficiency 病患感染導致休克,最適處理方式？",
        "option_a": "(A)去氧腎上腺素與抗生素",
        "option_b": "(B) IV hydrocortisone 與生理食鹽水",
        "option_c": "(C) ACTH 測試後決定治療",
        "option_d": "(D)注射長效類固醇",
        "correct_answer": "B",
        "explanation": "此為腎上腺危象(Adrenal crisis)引起的休克。應立即給予Hydrocortisone(同時具糖皮質素與部分鹽皮質素作用)並補足生理食鹽水。此時對升壓劑反應差，且不應因做測試而延誤急救。",
        "category": "腎上腺疾病:庫欣氏症候群及腎上腺機能不足 李美月"
    },
    {
        "id": 31,
        "question": "關於糖尿病患者之營養補充建議,下列何者最適當？",
        "option_a": "(A)應常規補充維生素與礦物質,以改善血糖控制",
        "option_b": "(B)補充鉻,或肉桂與蘆薈等草本成分,可作為血糖穩定之建議策略",
        "option_c": "(C)服用 Metformin者,應定期檢測維生素B12狀態,以預防缺乏",
        "option_d": "(D)建議例行補充β-胡蘿蔔素,以減少氧化壓力與神經病變風險",
        "correct_answer": "C",
        "explanation": "長期服用Metformin與維生素B12缺乏具有相關性，應定期監測。ADA指南不推薦常規補充微量元素、草本植物或β-胡蘿蔔素來管理血糖。",
        "category": "內分泌營養學 黃孟娟"
    },
    {
        "id": 32,
        "question": "下列關於糖尿病及肥胖相關之體重管理建議,下列何者最適當？",
        "option_a": "(A) Prediabetes (糖尿病前期)減少體重至少3-7%有助於降低進展為第2型法",
        "option_b": "(B) Diabetes (糖尿病)減少體重至少5%以上有助於血糖、血脂及血壓的改善",
        "option_c": "(C)對於BMI >=30.0 的肥胖患者,飲食運動調整、藥物治療與代謝手術均可考慮",
        "option_d": "(D)以上皆是",
        "correct_answer": "D",
        "explanation": "根據指引，糖尿病前期減重3-7%、糖尿病減重>=5%皆能帶來顯著臨床效益；當華人BMI>=30(肥胖)時，飲食、運動、藥物及手術皆為可採行的治療策略。",
        "category": "內分泌營養學 黃孟娟"
    },
    {
        "id": 33,
        "question": "關於糖尿病病人碳水化合物攝取之衛教與管理,下列何者最適當？",
        "option_a": "(A)病人可透過碳水化合物總克數監測、六大類食物份數代換或醣類計算指導,來協助血糖控制與自我管理",
        "option_b": "(B)只要避免甜點與含糖飲料,即無需監測每日總碳水化合物攝取量",
        "option_c": "(C)水果與全穀類富含膳食纖維,在衛教時可不納入醣類計算",
        "option_d": "(D)奶類富含乳糖,在衛教時可不納入醣類計算",
        "correct_answer": "A",
        "explanation": "六大類食物中，主食、水果、奶類皆富含醣類會影響血糖，皆必須納入醣類計算(carbohydrate counting)中，不能僅靠避開甜點飲料。",
        "category": "內分泌營養學 黃孟娟"
    },
    {
        "id": 34,
        "question": "關於核子醫學敘述,何者最不適當？",
        "option_a": "(A)主要特色是利用示蹤劑的原理,呈現功能性影像",
        "option_b": "(B)核子醫學甲狀腺掃描可以協助偵測異位性甲狀腺組織",
        "option_c": "(C)針對甲狀腺掃描,Pinhole準直儀可以有放大的效果",
        "option_d": "(D)平面影像即可精準做病灶定位。單光子射出電腦斷層技術(SPECT)收集影像很花時間,實在沒有必要",
        "correct_answer": "D",
        "explanation": "SPECT/CT能夠大幅增進病灶定位的精確度（例如精確定位極微小的parathyroid adenomas），在臨床上非常必要。",
        "category": "內分泌系統的放射免疫分析與核醫影像學 張晉銓"
    },
    {
        "id": 35,
        "question": "關於RIA和IRMA的比較,何者最不適當？",
        "option_a": "(A) RIA 中同位素標記抗原;IRMA 中同位素標記抗體",
        "option_b": "(B)在IRMA中,標記抗體是過量的,而且不存在競爭性結合複雜的反應,所以反應速度較RIA快",
        "option_c": "(C) RIA 為非競爭結合,劑量反應曲線為正相關的直線關係;IRMA為競爭抑制,測得的放射線活性與受檢抗原成反比",
        "option_d": "(D) RIA 應用多株抗體,親和力和特異性要求較高,但用量很少;IRMA中標記抗體和固相抗體用量較多,一般使用來源豐富、特異性較高的單株抗體",
        "correct_answer": "C",
        "explanation": "RIA為競爭結合原理，測得活性與受檢抗原成反比；IRMA為直接結合（非競爭），活性與受檢抗原成正比。選項C的敘述完全顛倒，故不適當。",
        "category": "內分泌系統的放射免疫分析與核醫影像學 張晉銓"
    },
    {
        "id": 36,
        "question": "副甲狀腺功能亢進症的核醫診斷工具,最常使用哪種示蹤劑？",
        "option_a": "(A) Tc-99m MDP",
        "option_b": "(B) Tc-99m Sestamibi",
        "option_c": "(C) I-123",
        "option_d": "(D) Ga-68 DOTATATE",
        "correct_answer": "B",
        "explanation": "副甲狀腺的Oxyphil cells富含粒線體，而Tc-99m Sestamibi (MIBI)會特異性附著在粒線體，常用於副甲狀腺亢進病灶之定位。",
        "category": "內分泌系統的放射免疫分析與核醫影像學 張晉銓"
    },
    {
        "id": 37,
        "question": "關於核子醫學1-123 MIBG 掃描的敘述,何者最為適當？",
        "option_a": "(A)通常不需要任何藥物前處理",
        "option_b": "(B)對甲狀腺腫瘤特異性極高",
        "option_c": "(C)可評估嗜鉻細胞瘤與副神經節瘤(paraganglioma)",
        "option_d": "(D)半衰期長,主要用於治療而非診斷",
        "correct_answer": "C",
        "explanation": "MIBG是norepinephrine類似物，會被吸收到交感節前細胞質內儲存小泡，可用於評估髓質來源的嗜鉻細胞瘤。術前需給予SSKI(碘片)進行甲狀腺保護阻斷。",
        "category": "內分泌系統的放射免疫分析與核醫影像學 張晉銓"
    },
    {
        "id": 38,
        "question": "關於 Tc-99m pertechnetate 之甲狀腺造影,何者最為適當？",
        "option_a": "(A)可反映甲狀腺結節的功能狀態",
        "option_b": "(B)可被甲狀腺有機化",
        "option_c": "(C)可以準確估算甲狀腺攝取碘的能力",
        "option_d": "(D)對兒童具有較高的輻射劑量",
        "correct_answer": "A",
        "explanation": "Tc-99m pertechnetate具有輻射劑量低、計數率高的優點（適合兒童），可反映結節功能狀態，但其缺點為「無法被有機化（not organified）」。",
        "category": "內分泌系統的放射免疫分析與核醫影像學 張晉銓"
    },
    {
        "id": 39,
        "question": "關於 Graves' disease的敘述,下列何者最為適當？",
        "option_a": "(A)為甲狀腺低下的常見原因",
        "option_b": "(B)可在掃描中看到斑塊狀冷結節",
        "option_c": "(C)通常合併甲狀腺縮小與低 RAIU",
        "option_d": "(D)常見於中年人,甲狀腺彌漫性腫大,%RAIU顯著升高",
        "correct_answer": "D",
        "explanation": "Graves' disease為甲狀腺亢進主因，影像特徵為瀰漫性腫大(diffusely enlarged)且%RAIU顯著升高(通常達50%-80%)。",
        "category": "內分泌系統的放射免疫分析與核醫影像學 張晉銓"
    },
    {
        "id": 40,
        "question": "對於嗜鉻細胞瘤(Pheochromocytoma),下列敘述何者錯誤？",
        "option_a": "(A)這類病人建議使用離子性顯影劑",
        "option_b": "(B)病人可能沒有症狀",
        "option_c": "(C)腫瘤有可能是惡性",
        "option_d": "(D)磁振造影在正反相位成像(In-Phase/Out-of-Phase Imaging)看不到訊號喪失",
        "correct_answer": "A",
        "explanation": "嗜鉻細胞瘤患者若使用離子性顯影劑(ionic contrast)具有誘發高血壓危象(hypertensive crisis)的風險，因此臨床建議使用非離子性顯影劑(nonionic)。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 41,
        "question": "下列敘述何者為誤？",
        "option_a": "(A)下視丘是間腦的一部分,位於丘腦之下",
        "option_b": "(B)腦下垂體的微腺瘤(microadenoma),指的是2公分以下",
        "option_c": "(C)如果下視丘與腦下垂體有懷疑的病灶,顯影的磁振造影檢查是首選",
        "option_d": "(D)磁振造影可以清楚看到下視丘及腦下垂體的構造",
        "correct_answer": "B",
        "explanation": "在腦下垂體腺瘤中，微腺瘤(microadenoma)定義上指的是直徑小於 1 cm（而不是2公分）。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 42,
        "question": "下列哪一項疾病可以被下岩樣竇採樣 Inferior petrosal sinus sampling 診斷？",
        "option_a": "(A)胰島細胞腫瘤 Pancreatic islet cell tumors",
        "option_b": "(B)腎上腺腺瘤 Adrenal adenoma",
        "option_c": "(C)嗜鉻細胞瘤 Pheochromocytoma",
        "option_d": "(D)腦下垂腺腺瘤 Pituitary adenoma",
        "correct_answer": "D",
        "explanation": "下岩樣竇採樣(BIPSS)用來測量腦下垂體激素(ACTH)的輸出量，主要用以鑑別與診斷腦下垂體腺瘤(Cushing's disease)或異位性分泌。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 43,
        "question": "下列關於影像診斷學的敘述,何者錯誤？",
        "option_a": "(A)評估腦下垂體腫瘤不須使用磁振造影 MRI檢查",
        "option_b": "(B)不同的解剖構造需要不同的影像學檢查",
        "option_c": "(C)可以提供正確的病灶偵測跟分期",
        "option_d": "(D)電腦斷層是一個評估腎上腺腫瘤良惡性的好工具",
        "correct_answer": "A",
        "explanation": "針對下視丘、腦下垂體區域的解剖構造與病灶評估，磁振造影(MRI)是臨床首選的檢查工具。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 44,
        "question": "下列對於腎上腺腺瘤 adrenal adenoma 的描述,何者錯誤？",
        "option_a": "(A)通常小於三公分",
        "option_b": "(B)未打顯影劑的電腦斷層(CT)檢查多呈現大於20HU 的數值",
        "option_c": "(C)絕對顯影喪失比例(Absolute percentage of enhancement loss)大於50%(或 60%)",
        "option_d": "(D)在正反相位成像大多看到訊號喪失",
        "correct_answer": "B",
        "explanation": "富含脂質的良性腎上腺腺瘤(Adrenal adenoma)，在未施打顯影劑的CT(unenhanced CT)下，衰減值典型上會「小於等於 10 HU」。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 45,
        "question": "對於 Multiple endocrine neoplasia (MEN) 1 敘述,何者為真？",
        "option_a": "(A)第十一對染色體缺失(Chromosome 11 defect)",
        "option_b": "(B)體染色體隱性(Autosomal Recessive)",
        "option_c": "(C)又稱 Sipple Syndrome",
        "option_d": "(D)主要症狀為原發性副甲狀腺功能亢進(Primary Hyperparathyroidism)、嗜鉻細胞瘤(Pheochromocytoma)、和甲狀腺髓樣癌(Medullary Thyroid Cancer, MTC)",
        "correct_answer": "A",
        "explanation": "MEN 1 (Wermer syndrome) 屬於體染色體顯性遺傳，由第11對染色體(11q13)缺陷所致。Sipple syndrome指的是MEN 2A。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 46,
        "question": "下列哪一項影像學特徵不是惡性甲狀腺結節較為常見的超音波影像學發現？",
        "option_a": "(A)低回音性結節 Hypoechoic nodule.",
        "option_b": "(B)微細鈣化點 Microcalcifications.",
        "option_c": "(C)彗星尾巴 Comet tail sign",
        "option_d": "(D)不規則邊界 Irregular border",
        "correct_answer": "C",
        "explanation": "超音波下出現「彗星尾巴」特徵(Comet tail artifact)是強烈支持為良性結節的影像學發現。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 47,
        "question": "對於甲狀腺超音波導引細針穿刺(ultrasound guided fine needle aspiration),下列敘述何者錯誤？",
        "option_a": "(A)選用超音波探頭7.5-15MHz 比選用2-5 MHz 來的適當",
        "option_b": "(B)選用細針 18gauge 的針頭是適當的粗細",
        "option_c": "(C)是一安全且有效診斷甲狀腺惡性結節的檢查",
        "option_d": "(D)血腫是穿刺後可能發生的併發症",
        "correct_answer": "B",
        "explanation": "細針穿刺(FNA)所選用的適當細針粗細範圍應為 22- to 27-gauge。18-gauge 太粗了。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 48,
        "question": "對於內分泌腫瘤的影像學特徵,下列何者錯誤？",
        "option_a": "(A)甲狀腺腫瘤若有結節內血流 intranodular blood flow,比較有可能是惡性",
        "option_b": "(B)胰臟的胰島素瘤大多血管豐富 hypervascular",
        "option_c": "(C)依賴 ACTH 的庫欣症候群 ACTH-dependent Cushing's syndrome 大多數可以看到單側的腎上腺增生 unilateral adrenal hyperplasia",
        "option_d": "(D)胃泌素瘤 Gastrinoma 通常不位於胰臟的尾部 Pancreatic tail",
        "correct_answer": "C",
        "explanation": "ACTH-dependent庫欣症候群是由於ACTH過量，會同時刺激雙側的腎上腺皮質，因此影像上典型會看到雙側瀰漫性增生(bilateral diffuse hyperplasia)。",
        "category": "內分泌疾病的電腦斷層和核磁共振影像學 (骨骼影像學) 蔡欣學"
    },
    {
        "id": 49,
        "question": "關於甲狀腺功能異常(Thyroid Dysfunction)的敘述,何者最為正確？",
        "option_a": "(A)成人甲狀腺功能低下症(Hypothyroidism) 常見突眼(exophthalmos)",
        "option_b": "(B)呆小病(Cretinism)因缺乏甲狀腺素(thyroid hormone)造成智力遲緩與生長遲滯",
        "option_c": "(C)黏液水腫(Myxedema)為甲狀腺功能亢進(hyperthyroidism) 引起的水腫",
        "option_d": "(D)大多數甲狀腺功能低下患者血中促甲狀腺激素(TSH)會下降",
        "correct_answer": "B",
        "explanation": "(A)突眼多見於甲狀腺亢進(Graves)。(C)黏液水腫是開發於嬰幼兒之後的成人甲狀腺低下表現(Gull disease)。(D)大多數低下患者因為缺乏回饋抑制，血中TSH會上升。",
        "category": "甲狀腺病理學 許又中"
    },
    {
        "id": 50,
        "question": "一位年輕女性出現突眼(exophthalmos)、心悸(palpitations)與體重減輕,甲狀腺切片組織學顯示高度增生、濾泡細胞排列呈乳突狀但無毛玻璃狀核。最可能的診斷為？",
        "option_a": "(A)乳突狀甲狀腺癌 (Papillary thyroid carcinoma)",
        "option_b": "(B)葛雷夫氏病(Graves disease)",
        "option_c": "(C)橋本氏甲狀腺炎(Hashimoto thyroiditis)",
        "option_d": "(D)亞急性甲狀腺炎(Subacute thyroiditis)",
        "correct_answer": "B",
        "explanation": "突眼、心悸、體重減輕合併組織學上經典的瀰漫性乳突狀增生(膠質邊緣呈鋸齒抽吸狀)，為Graves disease的典型表現。",
        "category": "甲狀腺病理學 許又中"
    },
    {
        "id": 51,
        "question": "一位40歲女性因頸部無痛性腫塊就醫,切片病理顯示大量乳突結構，分支明顯且具有纖細的纖維血管核心。最可能診斷為？",
        "option_a": "(A)濾泡狀癌(Follicular carcinoma)",
        "option_b": "(B)乳突狀甲狀腺癌 (Papillary thyroid carcinoma)",
        "option_c": "(C)髓樣癌(Medullary thyroid carcinoma)",
        "option_d": "(D)葛雷夫氏病(Graves disease)",
        "correct_answer": "B",
        "explanation": "頸部無痛性腫塊，組織學上呈現分支發達的Papillary carcinoma結構，對應乳突狀甲狀腺癌。",
        "category": "甲狀腺病理學 許又中"
    },
    {
        "id": 52,
        "question": "關於下列甲狀腺腫瘤(thyroid neoplasms)與基因突變(genetic mutations)的配對,何者最為正確？",
        "option_a": "(A) Papillary carcinoma - RET/NTRK rearrangement or BRAF V600E mutation",
        "option_b": "(B) Medullary carcinoma - PAX8-PPARY fusion gene",
        "option_c": "(C) Follicular carcinoma - RET mutation",
        "option_d": "(D) Anaplastic carcinoma commonly shows PSA positivity",
        "correct_answer": "A",
        "explanation": "Papillary甲狀腺癌經典的基因變異包含RET或NTRK的易位融合，以及BRAF點突變(BRAF V600E)。Medullary應配RET mutation；Follicular配PAX8-PPARY fusion。",
        "category": "甲狀腺病理學 許又中"
    },
    {
        "id": 53,
        "question": "一位60歲男性有高血鈣(hypercalcemia)與低血磷(hypophosphatemia),X光顯示骨質疏鬆。副甲狀腺切片顯示單一病灶,由均一的主細胞(chief cells)組成;無明顯脂肪。最可能診斷為？",
        "option_a": "(A)副甲狀腺增生(Parathyroid hyperplasia)",
        "option_b": "(B)副甲狀腺癌(Parathyroid carcinoma)",
        "option_c": "(C)副甲狀腺腺瘤(Parathyroid adenoma)",
        "option_d": "(D)髓樣癌(Medullary thyroid carcinoma)",
        "correct_answer": "C",
        "explanation": "高血鈣低血磷(副甲狀腺亢進)伴隨單一、邊界清晰的 soft tan nodule，組織學由均一主細胞組成且內部缺乏脂肪，符合副甲狀腺腺瘤特徵。",
        "category": "副甲狀腺病理學 許又中"
    },
    {
        "id": 54,
        "question": "關於副甲狀腺腺瘤(Parathyroid adenoma)的敘述,下列何者最為正確？",
        "option_a": "(A)常見多發性病灶,侵犯四個腺體",
        "option_b": "(B)組織學常見囊膜侵犯(capsular invasion)",
        "option_c": "(C)通常由主細胞(chief cells) 構成,病灶邊緣可見壓迫正常組織",
        "option_d": "(D)病灶中脂肪含量明顯高於正常副甲狀腺組織",
        "correct_answer": "C",
        "explanation": "副甲狀腺腺瘤典型以「單一腺體」病變為主，病灶邊緣可見一層被壓迫的正常非新生物副甲狀腺組織(A rim of compressed non-neoplastic tissue)，且內部脂質比正常組織少。",
        "category": "副甲狀腺病理學 許又中"
    },
    {
        "id": 55,
        "question": "對於甲狀腺亢進的描述何者為非？",
        "option_a": "(A)好發於女性",
        "option_b": "(B)葛雷夫氏症最常見",
        "option_c": "(C)好發年齡在超過60歲者",
        "option_d": "(D)可使用藥物或碘131治療",
        "correct_answer": "C",
        "explanation": "甲狀腺亢進(如Graves' disease)的典型好發發病年齡通常分布在 20 到 40 歲之間，並非以大於60歲為主群。",
        "category": "甲狀腺高能症及低能症 盧介祥"
    },
    {
        "id": 56,
        "question": "對於甲狀腺低下的描述何者為非？",
        "option_a": "(A)好發於女性年齡在超過60歲者",
        "option_b": "(B)可能是先天性或與自體免疫疾病有關",
        "option_c": "(C)可發生於開刀、藥物或碘131治療後",
        "option_d": "(D)不用治療",
        "correct_answer": "D",
        "explanation": "甲狀腺功能低下必須接受長期的甲狀腺激素替代療法（例如口服 levothyroxine）並常規監測功能，絕非不用治療。",
        "category": "甲狀腺高能症及低能症 盧介祥"
    },
    {
        "id": 57,
        "question": "對於亞臨床症狀甲狀腺低下的描述何者為非？",
        "option_a": "(A)最常見的原因是橋本氏疾病(Hashimoto's disease).",
        "option_b": "(B)常見好發於女性.",
        "option_c": "(C)實驗室檢查可見到TSH和FT4 高.",
        "option_d": "(D)可能與甲狀腺功能早期衰退有關.",
        "correct_answer": "C",
        "explanation": "亞臨床甲狀腺功能低下(Subclinical hypothyroidism)在實驗室檢查的定義是：血清 TSH 偏高，但是週邊 Free T4 與 T3 濃度完全處在「正常範圍」內。",
        "category": "甲狀腺高能症及低能症 盧介祥"
    },
    {
        "id": 58,
        "question": "下列何種甲狀腺癌最常見？",
        "option_a": "(A)乳突細胞癌",
        "option_b": "(B)濾泡細胞癌",
        "option_c": "(C)髓質細胞癌",
        "option_d": "(D)未分化細胞癌",
        "correct_answer": "A",
        "explanation": "乳突細胞癌(Papillary cancer)是目前最常見的甲狀腺惡性腫瘤，大約佔了所有病例的 80% 到 85%。",
        "category": "甲狀腺腫及甲狀腺癌 盧介祥"
    },
    {
        "id": 59,
        "question": "對於甲狀癌的描述何者為非？",
        "option_a": "(A)診斷可藉由觸診、超音波、核醫造影、細針穿刺",
        "option_b": "(B)甲狀腺超波可以提供快速正確的檢查",
        "option_c": "(C)甲狀腺核醫造影的熱點(hot nodule)會比冷點(cold nodule)癌症機會高",
        "option_d": "(D)甲狀腺癌的預後通常以乳突癌的預後最好",
        "correct_answer": "C",
        "explanation": "核醫甲狀腺掃描中的「熱點」(Hot nodule)在臨床上「幾乎從不(almost never)」代表顯著的惡性惡化；相反地，冷點(Cold nodule)伴隨有5%至15%的惡性風險。",
        "category": "甲狀腺腫及甲狀腺癌 盧介祥"
    },
    {
        "id": 60,
        "question": "甲狀腺癌的治療方式包括哪些？",
        "option_a": "(A)手術切除",
        "option_b": "(B)碘131",
        "option_c": "(C)化療或生物製劑(如 TKI 標靶藥物)",
        "option_d": "(D)以上皆是",
        "correct_answer": "D",
        "explanation": "甲狀腺癌的綜合內外科處置手段包含了外科切除術、放射性碘131治療、甲狀腺素抑制治療，以及針對晚期無法切除的酪胺酸激酶抑制劑(TKI)等標靶化療。",
        "category": "甲狀腺腫及甲狀腺癌 盧介祥"
    },
    {
        "id": 61,
        "question": "糖尿病酮酸血症(DKA)重症病患，出現T4與T3皆低下但TSH正常的表現，下列判讀何者正確？",
        "option_a": "(A)只要病患服用過 amiodarone，便應直接完全歸因於該藥物影響",
        "option_b": "(B)應建議立刻常規開立甲狀腺素給予補充治療",
        "option_c": "(C)重症引發大量細胞激素釋放進而抑制5'-去碘酵素(5'-deiodinase)為其重要核心機轉",
        "option_d": "(D)此種病態表現與疾病預後完全無關",
        "correct_answer": "C",
        "explanation": "重症病患出現「T3/T4低、TSH正常偏低」符合病態甲狀腺正能症(NTIS/Sick Euthyroid Syndrome)特徵。其主要成因是發炎細胞激素釋放，導致週邊5'-deiodinase活性受損以及荷爾蒙與結合蛋白親和力下降。臨床不主張給予甲狀腺素治療，應以監測與治療原發重症為主。",
        "category": "甲狀腺炎及病態甲狀腺正能症 洪薇雯"
    },
    {
        "id": 62,
        "question": "在病態甲狀腺正能症(NTIS)的臨床表現中，下列哪項指標最常被指出可用於評估重症病患的「不良預後(poor prognosis)」？",
        "option_a": "(A) TSH 濃度的短暫輕微波動",
        "option_b": "(B) 治療監測期間內測得的總 T4 濃度出現顯著劇烈滑落",
        "option_c": "(C) 僅有單純輕微的低 T3 表現",
        "option_d": "(D) 血沉降率(ESR)的單純波動",
        "correct_answer": "B",
        "explanation": "在NTIS中，低T3通常反映疾病嚴重度；而當病情嚴重到總T4水平也發生急劇大跌落(low T4 syndrome)時，在臨床上與病患的不良預後(poor prognosis)有著強烈關聯。",
        "category": "甲狀腺炎及病態甲狀腺正能症 洪薇雯"
    },
    {
        "id": 63,
        "question": "關於病態甲狀腺正能症(NTIS)的機轉描述，下列何者正確？",
        "option_a": "(A)體內甲狀腺荷爾蒙與結合蛋白(binding protein)的親和力下降(Decrease affinity)為核心原因之一",
        "option_b": "(B) T3 濃度愈低代表重症疾病的臨床嚴重度愈低",
        "option_c": "(C) 所有臨床重症表現皆是因為 amiodarone 代謝物之輕微拮抗作用引起的",
        "option_d": "(D) 以上敘述皆正確",
        "correct_answer": "A",
        "explanation": "NTIS的核心兩大機轉為：1. 甲狀腺荷爾蒙與結合蛋白間的親和力下降；2. 5'-deiodinase功能受損。T3越低代表病況越嚴重。",
        "category": "甲狀腺炎及病態甲狀腺正能症 洪薇雯"
    },
    {
        "id": 64,
        "question": "下列何者最能正確說明線性能量轉移(Linear Energy Transfer, LET)在放射治療中的作用？",
        "option_a": "(A)高LET 的輻射通常造成較少的生物傷害",
        "option_b": "(B)高LET 的輻射會產生更強烈密集性的電離作用,導致較嚴重的細胞與 DNA 損傷",
        "option_c": "(C)低LET 的輻射比高LET的輻射更易造成嚴重的DNA雙股斷裂",
        "option_d": "(D)放射線所引起的整體生物效應與其LET 值完全無關",
        "correct_answer": "B",
        "explanation": "速度慢且電荷數高的射線其LET高。高LET輻射會在組織路徑中引起極高密度的離子化作用，產生的生物效應也強烈，更容易造成細胞DNA重度損傷。",
        "category": "內分泌疾病的放射治療 湯人仰"
    },
    {
        "id": 65,
        "question": "關於垂體腫瘤放射治療後達到生化緩解(Biochemical remission)時間的典型對比，下列何者正確？",
        "option_a": "(A)傳統外照射放射治療(EBRT)通常比立體定位放射手術(SRS)更快達到生化緩解",
        "option_b": "(B)單次劑量 SRS 通常在16-26個月內達到生化緩解,而EBRT則常需大約63個月",
        "option_c": "(C)無論是 EBRT或SRS,兩者在一年內皆能可靠且普遍地使病患達到完全生化緩解",
        "option_d": "(D) EBRT 與 SRS 兩者在臨床上的生化緩解時間無任何統計學顯著差異",
        "correct_answer": "B",
        "explanation": "臨床數據顯示，立體定位放射手術(SRS)達到生化緩解的時間顯著快於傳統EBRT(SRS約16-26個月；EBRT常需長達63個月)。",
        "category": "內分泌疾病的放射治療 湯人仰"
    },
    {
        "id": 66,
        "question": "根據 NCCN 指南,下列哪一種臨床場景最明顯需要對甲狀腺癌進行外照射放射治療(EBRT)？",
        "option_a": "(A)手術後顯示良好碘131(131I)攝取能力的乳突狀癌",
        "option_b": "(B)僅有輕微腺體外侵犯的T2腫瘤",
        "option_c": "(C)低風險且完全無任何淋巴結侵犯的早期甲狀腺癌",
        "option_d": "(D)具有肉眼可見明顯甲狀腺外侵犯的T4原發性腫瘤",
        "correct_answer": "D",
        "explanation": "根據NCCN指引，EBRT用於甲狀腺癌的明確指徵包括：無法切除、局部復發病灶、肉眼可見的大體甲狀腺外侵犯(T4)腫瘤、或是手術後微觀/宏觀殘留且131I攝取能力不佳者。",
        "category": "內分泌疾病的放射治療 湯人仰"
    },
    {
        "id": 67,
        "question": "在鑑別輕度原發性副甲狀腺功能亢進(PHPT)與家族性低尿鈣高血鈣症(FHH)時,下列哪項檢查結果清單組合最倾向於支持FHH的診斷？",
        "option_a": "(A) 24小時尿鈣350mg,鈣清除率/肌酐清除率比值(ClCa/ClCr)為0.025",
        "option_b": "(B) 24小時尿鈣<100mg(如80mg),鈣清除率/肌酐清除率比值(ClCa/ClCr)<0.01(如0.008)",
        "option_c": "(C)血清 1,25(OH)2D3 濃度顯著異常升高",
        "option_d": "(D)骨密度DXA顯示所有部位T值皆顯著大於+1.0",
        "correct_answer": "B",
        "explanation": "家族性低尿鈣高血鈣症(FHH)的重要診斷特徵是24小時尿鈣排泄量低下(<100 mg/day)且鈣清除率/肌酐清除率比值(ClCa/ClCr)小於 0.01。",
        "category": "副甲狀腺高能症(高鈣血症) 盧子文"
    },
    {
        "id": 68,
        "question": "一位病患因乳癌骨轉移導致嚴重高血鈣 (15.0 mg/dL),醫師決定使用靜脈注射雙磷酸鹽治療。關於此治療，下列敘述何者錯誤？",
        "option_a": "(A)雙磷酸鹽能迅速(在給藥後數小時內)且強效地抑制蝕骨細胞活性,使血鈣立即降至正常",
        "option_b": "(B)常用的靜脈注射雙磷酸鹽藥物包括Pamidronate 和Zoledronate",
        "option_c": "(C)治療後血鈣通常在24至48小時內才開始逐步下降,並在一週內達到最低點",
        "option_d": "(D)需注意潛在的腎毒性,對於腎功能嚴重不全的患者應謹慎使用或避免使用",
        "correct_answer": "A",
        "explanation": "雙磷酸鹽(Bisphosphonates)雖然作用強效且持久，但是「起效緩慢」，通常需要 1~2 天(24-48小時)才會開始展現降鈣效果，並非在數小時內立刻神速起效。",
        "category": "副甲狀腺高能症(高鈣血症) 盧子文"
    },
    {
        "id": 69,
        "question": "一名60歲女性原發性副甲狀腺功能亢進患者，血鈣10.8mg/dL。根據目前的指引,下列哪項臨床數據是支持她接受副甲狀腺切除手術的最強理由？",
        "option_a": "(A)病患年齡剛好為 60 歲",
        "option_b": "(B) 24小時尿鈣排出量僅為 220 mg/day",
        "option_c": "(C) DXA 骨密度檢查顯示其遠端 1/3 橈骨(distal 1/3 radius)之 T 值為 -2.6",
        "option_d": "(D) 病患主觀上強烈拒絕外科介入",
        "correct_answer": "C",
        "explanation": "NIH無症狀原發性副甲狀腺亢進的手術指引包括：年齡<50歲、血鈣高於正常上限0.25 mmol/L、肌酐清除率<60 ml/min、24小時尿鈣>400 mg/d或有結石、以及骨密度DXA任一部位(腰椎、髖骨、股骨頸或遠端1/3橈骨) T-score < -2.5。該個案橈骨T值為-2.6(<-2.5)，符合手術適應症。",
        "category": "功能性腎上腺腫瘤之外科治療／甲、副甲狀腺疾病之外科治療 李香瑩／吳哲維"
    },
    {
        "id": 70,
        "question": "下列關於自體免疫多腺體症候群 Autoimmune Polyendocrine Syndrome (APS) type 1的敘述,何者為非？",
        "option_a": "(A)診斷的三個主特徵包含慢性皮膚黏膜念珠菌病、副甲狀腺功能低下、艾迪森氏症，須符合其中兩種",
        "option_b": "(B)此疾病皆是常染色體隱性,絕無任何AIRE基因（如CARD區）變異引發顯性遺傳的特例報告",
        "option_c": "(C) AIRE 基因若發生缺失突變,會導致胸腺 mTECs 無法正常表現特異抗原進而使T細胞無法完成株落刪除",
        "option_d": "(D)若病人合併原發性甲狀腺低下,可能會因為降低肝臟代謝效率而顯著延長體內皮質醇(cortisol)的半衰期",
        "correct_answer": "B",
        "explanation": "APS-1通常為自體隱性(21號染色體AIRE突變)，但目前已有少數自體顯性(autosomal dominant)的特殊突變被發現報告在AIRE基因的CARD或PHD1區域。故(B)敘述太過絕對而錯誤。此外，低下造成的肝代謝變慢會拉長cortisol半衰期，因此治療必須先補類固醇再補甲狀腺素，否則會誘發Adrenal crisis。",
        "category": "多腺體自體免疫疾病 許乃薇"
    },
    {
        "id": 71,
        "question": "下列關於自體免疫多腺體症候群 Autoimmune Polyendocrine Syndrome (APS) type 2的敘述,何者為非？",
        "option_a": "(A) APS type 2 通常好發在 20-60 歲的成年人群中",
        "option_b": "(B) 其艾迪森氏症(Addison's disease)的發病與家族內 HLA-DR3 及 HLA-DR4 具有強烈相關性",
        "option_c": "(C) 臨床統計上，APS type 2 最常見的兩種內分泌疾病配對必為艾迪森氏症與原發性性腺功能低下",
        "option_d": "(D) 抗 CD3 單株抗體 Teplizumab 可用於stage 2第一型糖尿病患者以延緩臨床發病",
        "correct_answer": "C",
        "explanation": "APS-2最常見的內分泌主要疾病組合成分是原發性腎上腺功能不全(Addison's, 50-70%)、自體免疫甲狀腺疾病(Graves/橋本, 15-69%)以及第一型糖尿病(40-50%)，原發性性腺功能低下發病率相對並非前二大，故(C)不正確。(此題因學術定義爭議在考場判定送分，原選項為C)",
        "category": "多腺體自體免疫疾病 許乃薇"
    },
    {
        "id": 72,
        "question": "下列關於其他的自體免疫多腺體疾病的敘述,何者為非？",
        "option_a": "(A) IPEX 症候群的致病機轉和 FOXP3 基因的突變直接相關",
        "option_b": "(B) 胰島素自體免疫綜合症候群(IAS)的誘發在臨床上與治療甲腺亢進的藥物 methimazole 有關",
        "option_c": "(C) 免疫檢查點抑制劑(ICI)引起的第一型糖尿病中，約有 70% 的個案帶有 HLA-DR4 基因突變",
        "option_d": "(D) Kearns-Sayre 症候群(Kearns-Sayre syndrome)是一種典型遵循孟德爾規律、家族代代垂直遺傳的粒線體DNA疾病",
        "correct_answer": "D",
        "explanation": "Kearns-Sayre症候群(Kearns-Sayre syndrome)在絕大多數臨床病例中屬於「偶發性(sporadic)」的粒線體DNA大片段缺失突變，而非高度家族遺傳性疾病。",
        "category": "多腺體自體免疫疾病 許乃薇"
    },
    {
        "id": 73,
        "question": "組織病理學上，下列哪一項特徵是確診甲狀腺乳突狀癌(Thyroid papillary carcinoma)最關鍵且不可或缺的核病理判定要件？",
        "option_a": "(A) 腫瘤細胞圍繞並覆蓋具有纖細纖維血管核心的乳突狀結構(Branching papillae)",
        "option_b": "(B) 腫瘤內出現明顯的嗜酸性化生(Oxyphilic metaplasia/Hürthle cells)",
        "option_c": "(C) 存在明確且廣泛的血管侵犯(Vascular invasion)或囊膜侵犯",
        "option_d": "(D) 腫瘤細胞核呈現染色質極度細微稀疏的磨砂玻璃狀外觀(Ground-glass/Orphan Annie nuclei)並伴隨核溝或假包涵體",
        "correct_answer": "D",
        "explanation": "甲狀腺乳突狀癌(PTC)的診斷是完全基於特殊的「細胞核特徵」(Nuclear appearance: Orphan Annie eye nuclei、核溝 nuclear grooves、偽包涵體 pseudo-inclusions)。即使缺乏明顯的乳突架構(papillary architecture)，只要具備這些特異細胞核特徵即可確診。",
        "category": "內分泌系統病理實驗 韋又菁"
    },
    {
        "id": 74,
        "question": "一名48歲女性，臨床主訴高燒、全身疲勞與明顯頸部劇烈脖子痛，鏡檢發現甲狀腺泡遭受破壞並形成由多核巨細胞(Multinucleated giant cell)圍繞微小膠質池(Pools of colloids)的肉芽腫病灶。最可能的診斷為？",
        "option_a": "(A) 結節性甲狀腺腫 Nodular goiter",
        "option_b": "(B) 肉芽腫性/亞急性甲狀腺炎 Granulomatous / Subacute (de Quervain) thyroiditis",
        "option_c": "(C) 甲狀腺髓樣癌 Medullary carcinoma",
        "option_d": "(D) 橋本氏甲狀腺炎 Hashimoto thyroiditis",
        "correct_answer": "B",
        "explanation": "發燒、脖子痛合併病理切片上經典的 Pools of colloids 與 Multinucleated giant cell (多核巨細胞肉芽腫發炎反應)，為亞急性/肉芽腫性甲狀腺炎的組織學標準特徵。",
        "category": "內分泌系統病理實驗 韋又菁"
    },
    {
        "id": 75,
        "question": "在病理形態學切片檢視下，區分與鑑別甲狀腺濾泡狀腺瘤(Follicular adenoma)與濾泡狀癌(Follicular carcinoma)最關鍵的唯一診斷依據是什麼？",
        "option_a": "(A) 是否存在明確的腫瘤囊膜侵犯(Capsular invasion)或血管侵犯(Vascular invasion)",
        "option_b": "(B) 組織內濾泡排列結構(Follicular arrangement)的密集程度與大小變異",
        "option_c": "(C) 腫瘤細胞是否局部排列成真性乳突分支架構(Papillary arrangement)",
        "option_d": "(D) 腫瘤濾泡上皮細胞核的異型性與多形性非典型特徵",
        "correct_answer": "A",
        "explanation": "濾泡狀腺瘤與濾泡狀癌在細胞外觀與濾泡排列上可能極度相似。兩者在病理診斷上的分水嶺純粹取決於有無「包膜侵犯(Capsular invasion)」或「血管侵犯(Vascular invasion)」。",
        "category": "內分泌系統病理實驗 韋又菁"
    },
    {
        "id": 76,
        "question": "關於腎上腺組織解剖結構分層與其相對應分泌的主要生理賀爾蒙，下列描述何者正確？",
        "option_a": "(A) 腎上腺皮質球狀帶(Zona glomerulosa) 主要分泌兒茶酚胺(Catecholamines)",
        "option_b": "(B) 腎上腺皮質束狀帶(Zona fasciculata) 主要分泌糖皮質激素(Glucocorticoids/Cortisol)",
        "option_c": "(C) 腎上腺皮質網狀帶(Zona reticularis) 主要分泌鹽皮質激素(Mineralocorticoids)",
        "option_d": "(D) 腎上腺髓質(Medulla) 主要負責分泌性類固醇激素(Sex steroids)",
        "correct_answer": "B",
        "explanation": "口訣：GFR對應鹽糖性。球狀帶(G)分泌鹽皮質激素(Aldosterone)；束狀帶(F)分泌糖皮質激素(Cortisol)；網狀帶(R)分泌性激素(Androgens)。髓質則負責分泌兒茶酚胺。",
        "category": "功能性腎上腺腫瘤之外科治療 李香瑩"
    },
    {
        "id": 77,
        "question": "依據現行國際篩檢臨床指引，下列哪種高血壓臨床表現的患者，「最不需要」常規接受原發性醛固酮增多症(Primary Aldosteronism)的專門篩檢？",
        "option_a": "(A) 經聯合常規使用三種以上口服藥物仍難以控制的頑固型/抗藥性高血壓患者",
        "option_b": "(B) 影像學偶然發現合併有高血壓表現的腎上腺偶發瘤(Adrenal incidentaloma)患者",
        "option_c": "(C) 發病極早的早發性高血壓(<20歲)或伴隨有年輕中風家族史(<50歲)的患者",
        "option_d": "(D) 一名70歲常規高血壓病患，多次實驗室抽血生化顯示血清鉀離子濃度恆定為 5.0 mEq/L",
        "correct_answer": "D",
        "explanation": "原發性醛固酮增多症(PA)的典型生化特徵為低血鉀。選項(D)病患的血清鉀離子濃度5.0 mEq/L屬於完全正常甚至偏高，在缺乏其他強烈適應症(如抗藥性高血壓)下，最不需要常規篩檢PA。",
        "category": "功能性腎上腺腫瘤之外科治療 李香瑩"
    },
    {
        "id": 78,
        "question": "關於功能性腎上腺腫瘤之外科手術切除路徑與方式描述，下列何者「有誤」？",
        "option_a": "(A) 大型多中心醫學實證已證實，腹腔鏡後腹腔切除路徑的手術長期生存率與成功率顯著優於經腹腔切除路徑",
        "option_b": "(B) 單孔腹腔鏡腎上腺手術在術後傷口美觀滿意度上相較傳統多孔具有優勢",
        "option_c": "(C) 臨床若遭遇體積過大、高度懷疑惡性皮質癌或與周邊重要大血管相黏嚴重的困難腫瘤，應採取傳統開放式開腹手術",
        "option_d": "(D) 具體手術術式的選定需綜合考量患者腫瘤尺寸、體型肥胖度、既往腹部手術史、經濟負擔與術者經驗進行個體化裁量",
        "correct_answer": "A",
        "explanation": "考科藍實證醫學審查(Cochrane Review)指出，經後腹腔(Retroperitoneal)與經腹腔(Transperitoneal)兩種腹腔鏡腎上腺切除術相比，不論在手術死亡率、短期併發症、手術時間或失血量上「皆無統計學顯著差別」，後腹腔僅在術後恢復進食時間上稍微縮短。故A說後者顯著優於前者是錯誤的。",
        "category": "功能性腎上腺腫瘤之外科治療 李香瑩"
    },
    {
        "id": 79,
        "question": "關於甲狀腺腫瘤與外科手術處置之描述，以下敘述何者正確？",
        "option_a": "(A) 甲狀腺細針抽吸細胞學報告若落在2023 TBSRTC分類第三級之AUS/FLUS者，因惡性風險達13-30%，臨床應一律直接安排診斷性單側切除術(Diagnostic lobectomy)",
        "option_b": "(B) 達文西機械手臂輔助甲狀腺切除術，在大型臨床數據中已被證實相較於傳統開放式開放手術能大幅縮短手術操作時間",
        "option_c": "(C) 術中例行性且仔細地解剖並辨識出喉返神經(Recurrent laryngeal nerve, RLN)的位置，是公認降低術後聲帶麻痺併發症的強烈建議手段",
        "option_d": "(D) 甲狀腺術後若病患僅出現無法發出高音、音頻耐受度差的障礙，最有可能是手術結紮上極時造成上喉神經(Superior laryngeal nerve)的「內支(Internal branch)」損傷",
        "correct_answer": "C",
        "explanation": "A項AUS/FLUS首選多為重複抽吸或分子檢測，非一律開刀。B項達文西機械手臂手術通常因架設與路徑關係，操作時間「比傳統手術更長」。D項控制高音的環甲肌(CTM)是由上喉神經的「外支(EBSLN)」支配，內支主要負責聲門上方感覺，因此高音障礙是EBSLN外支損傷而非內支。C項術中辨識RLN為最高等級臨床指引強烈推薦。",
        "category": "甲狀腺及副甲狀腺疾病之外科治療 吳哲維"
    },
    {
        "id": 80,
        "question": "關於甲狀腺手術前，醫療團隊與病患進行術前知情同意(Informed consent)書內容說明時，以下敘述何者「為非」？",
        "option_a": "(A) 術後可能因為神經微觀損傷或水腫沾黏，出現暫時或永久性的音聲功能障礙(Dysphonia)",
        "option_b": "(B) 執行全甲狀腺切除術後，病患將面臨永久性甲狀腺功能低下(Hypothyroidism)，必須終身每日服用左旋甲狀腺素",
        "option_c": "(C) 術後若發生嚴重的全副甲狀腺功能低下，會導致體內發生急性低血磷(Hypophosphatemia)危象，病患將出現嚴重手足抽搐與肌肉麻痛",
        "option_d": "(D) 手術後24小時內(尤其是前6小時)需嚴密監控可能發生的頸部血腫(Hematoma)，若壓迫呼吸道造成窒息需立刻在床旁排空並緊急重返手術室探查",
        "correct_answer": "C",
        "explanation": "副甲狀腺功能低下(Hypoparathyroidism)會導致體內發生嚴重的「低血鈣(Hypocalcemia)」，進而引發手足搐搦(Tetany)、Chvostek's與Trousseau's sign，而非引起低血磷（副甲狀腺素下降在腎臟減少排磷，血磷反而傾向升高）。故C錯誤。",
        "category": "甲狀腺及副甲狀腺疾病之外科治療 吳哲維"
    },
    {
        "id": 81,
        "question": "關於副甲狀腺機能亢進(Hyperpreathyroidism, HPT)與外科手術處置，以下敘述何者為非？",
        "option_a": "(A) 原發性副甲狀腺機能亢進(Primary HPT)臨床上最常見的底層病因是惡性副甲狀腺癌(Carcinoma)，最常採取微創副甲狀腺切除術(MIP)進行根除",
        "option_b": "(B) 指引建議，針對臨床無症狀的原發性副甲狀腺機能亢進患者，若其年齡小於 50 歲，即使指標輕微也應採取更積極的手術切除考量",
        "option_c": "(C) 次發性副甲狀腺機能亢進(Secondary HPT)在臨床洗腎病患中極為常見，主要刺激源為慢性腎衰竭所致的低血鈣、高血磷以及活性維生素D缺乏",
        "option_d": "(D) 尿毒症患者在接受副甲狀腺全切除手術時，通常會例行將部分非腺瘤組織切碎，自體移植(Autotransplantation)於非優勢側前臂的肱橈肌(Brachioradialis muscle)內以利後續復發局部監控",
        "correct_answer": "A",
        "explanation": "原發性副甲狀腺機能亢進(PHPT)最常見的成因是良性的「單一腺瘤(Single Parathyroid Adenoma)」，佔了所有病例的 80-85%；惡性的副甲狀腺癌(Carcinoma)極其罕見，盛行率小於 1%。故A不正確。",
        "category": "甲狀腺及副甲狀腺疾病之外科治療 吳哲維"
    },
    {
        "id": 82,
        "question": "下列關於多發性內分泌腫瘤第一型 (MEN type 1) 的臨床與基因敘述，何者「正確」？",
        "option_a": "(A) 該症候群在臨床上最常見且最早出現的腫瘤表徵為甲狀腺髓樣癌(MTC)",
        "option_b": "(B) 該致病機轉主要是由於原癌基因 RET 發生了生殖細胞系外顯位點突變所致",
        "option_c": "(C) 該基因的外顯率(Penetrance)具有高度年齡依賴性，在病患 50 歲前外顯率高達約 98%",
        "option_d": "(D) 該症候群合併的腸胰內分泌腫瘤(Enteropancreatic tumor)中，臨床最常見的類型為胰島素瘤(Insulinoma)",
        "correct_answer": "C",
        "explanation": "MEN 1 (Wermer syndrome)是由位於11q13的MEN1抑癌基因突變引起，50歲前外顯率達98%（C正確）。最常見、最早出現的是副甲狀腺腺瘤(90%)；髓樣癌(MTC)與RET突變是屬於MEN 2A/2B的特徵。MEN 1的腸胰內分泌瘤中，以胃泌素瘤(Gastrinoma >50%)最常見，而非Insulinoma(10-30%)。",
        "category": "內分泌高血壓,多發性內分泌腫瘤／皮質醛酮高能症及低能症 歐昱侖"
    },
    {
        "id": 83,
        "question": "根據國際多發性內分泌腫瘤臨床處置指南，對於臨床上完全無症狀、但在基因篩檢中被證實帶有高危險度 RET 918 點突變（典型對應 MEN 2B）的兒童，建議何時接受預防性甲狀腺全切除術(Prophylactic thyroidectomy)？",
        "option_a": "(A) 延遲觀察直至年滿 5 歲之後再行評估",
        "option_a": "(B) 為了防止惡性度極高的髓樣癌早期轉移，強烈建議在嬰兒 1 歲之前執行出手術",
        "option_c": "(C) 進入青少年發育期(13-18歲)且超音波發現微小異常時再行切除",
        "option_d": "(D) 臨床觸診或頸部影像學明確查見實體腫塊時方採取外科介入",
        "correct_answer": "B",
        "explanation": "RET 918位點突變在MEN2變異中屬於最高危險度等級，其引發的甲狀腺髓樣癌(MTC)惡性度極高且會在嬰幼兒期極早期發生遠端轉移，因此指引強烈建議應在「1歲之前」執行預防性全甲狀腺切除術。",
        "category": "內分泌高血壓,多發性內分泌腫瘤／皮質醛酮高能症及低能症 歐昱侖"
    },
    {
        "id": 84,
        "question": "下列關於嗜鉻細胞瘤(Pheochromocytoma)的臨床特徵與圍手術期藥物準備敘述，何者正確？",
        "option_a": "(A) 經典的「十之法則(Rule of Tens)」包含：10%為單側發生、10%位於腎上腺內、10%發生遠端轉移",
        "option_b": "(B) 特異性功能診斷核醫影像定位可以考慮首選 I-101 MIBG 掃描檢查",
        "option_c": "(C) 該腫瘤惡性度極高，絕大多數個案即使經過完全的外科手術切除也完全無法達到臨床治癒",
        "option_d": "(D) 術前的血壓與藥物準備具有絕對嚴格的順序：必須「先使用 Alpha 受體阻斷劑」進行血管擴張，隨後才能加用 Beta 受體阻斷劑",
        "correct_answer": "D",
        "explanation": "Rule of Tens定義為：10%雙側(Bilateral)、10%腎上腺外(Extra-adrenal)、10%惡性轉移。核醫影像使用的是 I-123 MIBG scan。手術切除有將近90%的患者可達到完全治癒。圍手術期藥物準備順序極為關鍵：必須先給予 Alpha blocker 阻斷血管收縮，若先給 Beta blocker 會因為血管上缺乏拮抗而導致兒茶酚胺引發致命的高血壓危象。",
        "category": "內分泌高血壓,多發性內分泌腫瘤／皮質醛酮高能症及低能症 歐昱侖"
    },
    {
        "id": 85,
        "question": "關於先天性腎上腺增生症(Congenital Adrenal Hyperplasia, CAH)的不同酶缺陷型臨床表現對比，下列敘述何者「錯誤」？",
        "option_a": "(A) 21-hydroxylase 缺陷型與 11ß-hydroxylase 缺陷型的患兒，皆會因為皮質醇合成受阻出現腎上腺功能不全(Adrenal insufficiency)",
        "option_b": "(B) 17a-hydroxylase 缺陷型由於不影響鹽皮質激素前驅物，臨床上「不常」以急性的腎上腺危象休克(Adrenal crisis)作為首發表現",
        "option_c": "(C) 21-hydroxylase 缺陷型會導致類固醇合成路徑往右側偏走，進而引發嚴重的雄性素過量(Androgen excess)與女性胎兒男性化",
        "option_d": "(D) 11ß-hydroxylase 缺陷型由於醛固酮(Aldosterone)水平下降，在臨床上會典型伴隨嚴重的低血鈉與高血鉀(Hyperkalemia)表現",
        "correct_answer": "D",
        "explanation": "11ß-hydroxylase缺陷雖然會導致終端 Aldosterone 產量低下，但其會在上游引發強效鹽皮質激素前驅物「11-去氧皮質酮(DOC)」的龐大蓄積。DOC具有強烈的留鈉排鉀效果，因此在臨床上與21-hydroxylase型相反，11ß缺陷型會呈現「低血鉀、高血壓(Hypokalemic hypertension)」而非高血鉀，這也是鑑別此兩大主型的重要臨床關鍵。故D錯誤。",
        "category": "內分泌高血壓,多發性內分泌腫瘤／皮質醛酮高能症及低能症 歐昱侖"
    },
    {
        "id": 86,
        "question": "關於原發性醛固酮增多症(Primary Aldosteronism, PA)，下列哪一項為其在臨床生化檢查上的典型三大特徵配對？",
        "option_a": "(A) 高血鈣、高血磷、代償性呼吸性酸中毒",
        "option_b": "(B) 高血壓、低血鉀(Hypokalemia)與代謝性鹼中毒",
        "option_c": "(C) 體位性低血壓、高血鉀與嚴重代謝性酸中毒",
        "option_d": "(D) 嚴重全身水腫、低血鈉與容量耗竭性酸中毒",
        "correct_answer": "B",
        "explanation": "原發性醛固酮增多症的核心病理為醛固酮過度分泌，在遠端腎小管加強「留鈉、排鉀、排氫」的作用。因此其臨床三大標誌性特徵為：高血壓(鈉水滯留)、低血鉀(鉀離子排出過多引發乏力)以及代謝性鹼中毒(氫離子流失過多)。",
        "category": "內分泌高血壓,多發性內分泌腫瘤／皮質醛酮高能症及低能症 歐昱侖"
    },
    {
        "id": 87,
        "question": "一名46歲男性長期高血壓合併肌肉無力。實驗室檢查：ARR=55，生理食鹽水輸注試驗(Saline infusion test)後血清醛固酮仍高達 28 ng/dL。腹部CT呈現右側腎上腺有一顆1.5cm腺瘤。根據診療規範，病患下一步「最應先採取」的處置是？",
        "option_a": "(A) 安排 1123 MIBG scan 來確定右側腎上腺腺瘤是否具有內分泌功能",
        "option_b": "(B) 既然CT已明確查見右側 1.5 cm 腫瘤，應立刻直接安排外科開刀將右側腎上腺切除",
        "option_c": "(C) 進行侵入性的雙側腎上腺靜脈採樣(Adrenal venous sampling, AVS)以確立功能是否確實具側邊化偏向",
        "option_d": "(D) 無需任何進一步定位與處置，直接給予最高劑量升壓劑聯合治療",
        "correct_answer": "C",
        "explanation": "ARR>=20且確診試驗(Saline infusion test)陽性，已完全確診為原發性醛固酮增多症(PA)。雖然CT查見右側1.5cm腺瘤，但指引強調CT/MRI對於區分究竟是單側腺瘤(APA)或雙側特發性增生(IHA)的準確度極差（常有偶然瘤誤導）。在考慮單側切除術前，必須進行雙側腎上腺靜脈採樣(AVS)進行功能側邊化(Lateralization)鑑定，以避免切錯健康的單側。故下一步首選為C。",
        "category": "內分泌高血壓,多發性內分泌腫瘤／皮質醛酮高能症及低能症 歐昱侖"
    }
]

def generate_csv():
    # 決定檔案要儲存在哪裡（自動存在 main.py 所在的資料夾中）
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(current_dir, "questions.csv")
    
    # 定義 CSV 的 9 個欄位
    fieldnames = ["id", "question", "option_a", "option_b", "option_c", "option_d", "correct_answer", "explanation", "category"]
    
    # 開始寫入檔案，使用 utf-8-sig 以完美防堵微軟 Excel 的分格亂碼問題
    with open(target_path, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # 寫入第一列標頭
        writer.writeheader()
        
        # 逐題寫入
        for q in ALL_QUESTIONS_DATA:
            writer.writerow(q)
            
    print(f"🎉 恭喜！全套 87 題的 CSV 題庫已成功生成！")
    print(f"💾 檔案路徑：{target_path}")

if __name__ == "__main__":
    generate_csv()
