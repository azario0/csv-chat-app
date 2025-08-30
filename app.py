# app.py
import os
import uuid
from flask import Flask, render_template, request, session, redirect, url_for, flash
from dotenv import load_dotenv
import pandas as pd
from pandasai import SmartDataframe
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Initialization ---
load_dotenv()
app = Flask(__name__)

# --- Configuration ---
# It's crucial to set a secret key for session management
app.secret_key = os.urandom(24) 
UPLOAD_FOLDER = 'static/uploads'
CHART_FOLDER = 'static/charts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CHART_FOLDER'] = CHART_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CHART_FOLDER, exist_ok=True)

# --- PandasAI LLM Configuration ---
def get_llm():
    """Initializes and returns the LLM instance."""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
    
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        temperature=0,
    )

# --- Route Definitions ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            try:
                # Clear previous session data
                session.clear()

                filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Store file path and initialize chat history in session
                session['csv_path'] = filepath
                session['chat_history'] = []

                # Generate a preview of the dataframe
                df = pd.read_csv(filepath) if filename.endswith('.csv') else pd.read_excel(filepath)
                session['df_head'] = df.head().to_html(classes='table table-striped table-hover', justify='left')

                flash('File uploaded successfully! You can now ask questions.', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'danger')
                return redirect(request.url)
    
    # On GET request or after POST, render the template
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    # Ensure a file has been uploaded first
    if 'csv_path' not in session:
        return redirect(url_for('index'))

    question = request.form.get('question')
    if not question:
        flash('Please enter a question.', 'warning')
        return redirect(url_for('index'))

    filepath = session['csv_path']
    chat_history = session.get('chat_history', [])

    try:
        llm = get_llm()
        df = pd.read_csv(filepath) if filepath.endswith('.csv') else pd.read_excel(filepath)
        
        # Configure PandasAI to save charts to our static folder
        sdf = SmartDataframe(df, config={
            "llm": llm,
            "save_charts": True,
            "save_charts_path": app.config['CHART_FOLDER'],
            "open_charts": False
        })
        
        # Get the response
        response = sdf.chat(question)

        # Handle different response types from PandasAI
        answer = ""
        if isinstance(response, (pd.DataFrame, pd.Series)):
            answer = response.to_html(classes='table table-striped table-hover', justify='left')
        elif isinstance(response, str) and response.endswith('.png'):
            # This is a path to a chart. Let's make it web-accessible.
            chart_filename = os.path.basename(response)
            chart_url = url_for('static', filename=f'charts/{chart_filename}')
            answer = f'<img src="{chart_url}" alt="Generated Chart" class="img-fluid">'
        else:
            answer = str(response)

        # Append to chat history
        chat_history.append({'question': question, 'answer': answer})
        session['chat_history'] = chat_history

    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred: {str(e)}"
        chat_history.append({'question': question, 'answer': f'<div class="alert alert-danger">{error_message}</div>'})
        session['chat_history'] = chat_history

    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    # Clean up uploaded file and chart if they exist
    if 'csv_path' in session and os.path.exists(session['csv_path']):
        os.remove(session['csv_path'])
    
    # Clear session data
    session.clear()
    flash('Session has been reset. Please upload a new file.', 'info')
    return redirect(url_for('index'))

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)