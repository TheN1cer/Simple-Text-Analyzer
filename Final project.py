# 1. 讀取文章檔案
file_name = "article.txt"
with open(file_name, "r", encoding="utf-8") as file:
    text = file.read()
#清理標點符號及換行符號, punctuation包含了所有的標點符號。
import string
text = text.translate(str.maketrans("", "", string.punctuation)).replace("\n", " ")

# 2. 文字切割 (將字串轉為 List)
word_list = text.split(" ")

# 3. 過濾雜訊 (設定 Tuple 黑名單)
stop_words = ("is", "and", "the", "a", "of", "to", "in", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or", "from", "at", "which", "but", "not", "all", "we", "they", "their", "his", "her", "my", "your", "its")
filtered_words = []
for word in word_list:
    # 簡單的清理：將單字轉小寫，方便比對
    clean_word = word.lower()
    if clean_word not in stop_words:
        filtered_words.append(clean_word)

# 4. 統計字頻 (使用 Dict)
word_counts = {}
for word in filtered_words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# 5. 排序並輸出結果
result = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# 列印出所有單字的統計結果
for item in result:
    print(f"單字: {item[0]}, 出現次數: {item[1]}")