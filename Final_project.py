import string
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pdfplumber

#定義一個分析機CLASS，負責處理文字分析的邏輯
class TextAnalyzer:
    def __init__(self):
        self.text = ""             
        self.word_counts = {}       
        self.filtered_words = []  # 確保過濾後的清單能被外部讀取
        
        # 預設的停用詞列表
        self.stop_words = (
            "is", "and", "the", "a", "of", "to", "in", "that", "it", "with", 
            "as", "for", "was", "on", "are", "by", "this", "be", "or", "from", 
            "at", "which", "but", "not", "all", "we", "they", "their", "his", 
            "her", "my", "your", "its", ""
        )

    # 讀取檔案內容，確定檔案格式為 txt 或 pdf，並將內容存入 self.text
    def load_file(self, file_path):
        self.text = ""  
        try:
            if file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text = file.read()
                return True
            elif file_path.lower().endswith(".pdf"):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text: 
                            self.text += page_text + "\n"
                return True
            return False
        except Exception as e:
            print(f"讀取錯誤: {e}")
            return False

    def process_text(self, custom_stopwords_str=""):

        #接收前端傳入的自訂停用詞字串（以逗號隔開）
        if not self.text:
            return

        # 1. 資料清洗
        clean_text = self.text.translate(str.maketrans("", "", string.punctuation)).replace("\n", " ")
        word_list = clean_text.split(" ")

        # 2. 處理前端傳過來的自訂過濾字 (轉小寫、去空白、用 set 加速比對)
        custom_set = set()
        if custom_stopwords_str:
            custom_set = {w.strip().lower() for w in custom_stopwords_str.split(",") if w.strip()}

        # 3. 過濾停用詞（內建黑名單 + 使用者自訂黑名單）
        self.filtered_words = []
        for word in word_list:
            clean_word = word.lower().strip()
            if clean_word not in self.stop_words and clean_word not in custom_set:
                self.filtered_words.append(clean_word)

        # 4. 迴圈統計次數
        self.word_counts = {}
        for word in self.filtered_words:
            if word in self.word_counts:
                self.word_counts[word] += 1
            else:
                self.word_counts[word] = 1

    #生成圖表，包含 CSV、長條圖、文字雲
    def generate_reports(self, limit=20):
        
        if not self.word_counts:
            return

        # 依照詞頻排序，取前 limit 個關鍵字
        sorted_result = sorted(self.word_counts.items(), key=lambda x: x[1], reverse=True)
        top_words = [item for item in sorted_result if len(item[0]) > 2][:limit]

        if len(top_words) == 0:
            return

        # 用pandas產出CSV檔，並且用utf-8-sig編碼確保Excel能正確讀取中文
        df = pd.DataFrame(top_words, columns=['Keyword', 'Frequency'])
        df.to_csv("keyword_report.csv", index=False, encoding="utf-8-sig")

        # --- 【長條圖獨立產出】 ---
        words = df['Keyword'].tolist()
        values = df['Frequency'].tolist()
        
        plt.figure(figsize=(14, 6))  # 寬高
        plt.bar(words, values, color='skyblue')
        plt.title(f"Top {limit} Keywords Analysis", fontsize=16, pad=15)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=11)  # 傾斜 45 度並向右對齊，避免字體疊在一起
        plt.tight_layout()
        plt.savefig("bar_chart.png")
        plt.close()

        # --- 【文字雲獨立產出】 ---
        plt.figure(figsize=(10, 6))
        wc = WordCloud(width=1000, height=600, background_color='white', colormap='viridis') #colormap='viridis' 讓顏色更柔和
        wc.generate_from_frequencies(self.word_counts)
        plt.imshow(wc, interpolation='bilinear')  #bilinear 讓圖像更平滑
        plt.axis('off')
        plt.title("Keyword Word Cloud", fontsize=16, pad=15)
        plt.tight_layout()
        plt.savefig("wordcloud.png")
        plt.close()