name: Hourly News Update
on:
  schedule:
    - cron: '*/10 * * * *' # Runs every 10 mins
  workflow_dispatch:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Updated from v3 to v4
      - uses: actions/checkout@v4 
      
      # Updated from v4 to v5
      - name: Set up Python
        uses: actions/setup-python@v5 
        with:
          python-version: '3.11' # Using a modern Python version too
          
      - name: Install deps
        run: pip install -r requirements.txt
        
      - name: Run Bot
        env:
          GEMINI_KEY: ${{ secrets.GEMINI_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
        run: python news_bot.py
