# Chat with Customer Data

A simple tool to ask questions about Excel data using AI.

## What it does

- Upload any Excel file
- Ask questions in plain English
- Get answers based on your data

## How it works

1. User uploads an Excel file
2. User types a question like "How many customers have budget above 90 lakhs?"
3. The app uses Gemini AI to understand the question
4. It converts the question to Python code
5. Runs the code on your data
6. Shows the answer

## Files in this project

```
chat-with-customer-data/
├── app.py              # Main application
├── query_engine.py     # Handles AI and data processing
├── data_loader.py      # Loads Excel files
├── requirements.txt    # Required packages
└── README.md           # This file
```

## How to setup and run

### Step 1: Clone this project
```bash
git clone https://github.com/nikitathapa1939/chat-with-customer-data.git
cd chat-with-customer-data
```

### Step 2: Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install packages
```bash
pip install -r requirements.txt
```

### Step 4: Add your Gemini API key
Open `app.py` and add your API key on line 11:
```python
API_KEY = "your_api_key_here"
```

Get free API key from: https://makersuite.google.com/app/apikey

### Step 5: Run the app
```bash
streamlit run app.py
```

App opens at http://localhost:8501

## How to use

1. Click "Browse files" and select your Excel file
2. Type your question
3. Click "Get Answer"
4. See the result

## Example questions

- How many records are there?
- What is the average budget?
- List customers in Pune
- How many customers have budget above 50 lakhs?
- Which location has the most customers?

## Technologies used

- Python
- Streamlit
- Pandas
- Google Gemini AI
