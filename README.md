# 八字命理諮詢系統

以四柱八字為核心的命理諮詢 Web 應用程式，畢業專題作品。整合微調後的 GPT 模型，提供個人化的年運、月運分析與即時命理問答。

## 功能

- 使用者註冊／登入
- 輸入生日與出生時間後自動排出四柱八字、納音、十神
- 年運分析：逐月大運批論
- 今日八字查詢
- GPT 命理對話（基於微調模型 ft:gpt-3.5-turbo / gpt-4o）

## 技術棧

- Python 3 / Django 5
- OpenAI API（微調模型 + gpt-4o）
- SQLite
- cnlunar（農曆 / 天干地支計算）

## 快速開始

```bash
pip install -r requirements.txt
cp .env.example .env   # 填入 OPENAI_API_KEY 與 DJANGO_SECRET_KEY
python manage.py migrate
python manage.py runserver
```

## 環境變數

| 變數 | 說明 |
|------|------|
| `OPENAI_API_KEY` | OpenAI API 金鑰 |
| `DJANGO_SECRET_KEY` | Django 應用程式密鑰 |
| `EMAIL_HOST_USER` | 寄件信箱（選填） |
| `EMAIL_HOST_PASSWORD` | 寄件信箱密碼（選填） |
