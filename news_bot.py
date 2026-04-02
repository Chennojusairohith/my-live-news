import os
import feedparser
import google.generativeai as genai
from supabase import create_client

# Load keys from GitHub Secrets
gemini_key = os.environ.get("GEMINI_KEY")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash')
supabase = create_client(supabase_url, supabase_key)

def update_news():
    # Fetching from The Hindu RSS
    feed = feedparser.parse("https://www.thehindu.com/news/national/feeder/default.rss")
    
    for entry in feed.entries[:5]:
        # AI creates a short summary
        prompt = f"Summarize this in 1 short sentence: {entry.title}. {entry.description}"
        response = model.generate_content(prompt)
        
        data = {
            "headline": entry.title,
            "summary": response.text.strip(),
            "link": entry.link
        }
        # Save to database
        supabase.table("live_news").upsert(data, on_conflict="link").execute()

if __name__ == "__main__":
    update_news()
