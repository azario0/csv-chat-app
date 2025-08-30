# CSV Chat AI 🤖

A sleek Flask web application that allows you to have a conversation with your CSV or Excel files. Upload your data, and use natural language to ask questions, generate insights, and visualize information with charts, all powered by Google's Gemini model through PandasAI.

This project was built to demonstrate the power of Large Language Models in creating intuitive data analysis tools.

## Preview


*(A sample GIF showing the upload and chat process with a chart response)*

---

## ✨ Features

-   **File Upload**: Supports both `.csv` and `.xlsx` file formats.
-   **Natural Language Queries**: Ask complex questions about your data without writing any code.
-   **Multiple Response Types**: Get answers as plain text, formatted tables, or beautiful charts (pie charts, bar graphs, etc.).
-   **Interactive Chat Interface**: A clean, modern UI to see your conversation history.
-   **Data Preview**: Instantly see the first few rows of your uploaded data to ensure it's loaded correctly.
-   **Session Management**: Your uploaded file and chat history are maintained for your session.
-   **Easy Reset**: Start over with a new file with a single click.

## 🛠️ Tech Stack

-   **Backend**: [Flask](https://flask.palletsprojects.com/)
-   **AI/LLM Integration**: [PandasAI](https://github.com/gventuri/pandas-ai), [LangChain](https://www.langchain.com/) (`langchain-google-genai`)
-   **Large Language Model**: Google Gemini 1.5 Flash
-   **Frontend**: HTML, [Bootstrap 5](https://getbootstrap.com/), Jinja2
-   **Data Handling**: [Pandas](https://pandas.pydata.org/)
-   **Plotting**: [Matplotlib](https://matplotlib.org/)

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

-   Python 3.8+
-   A Google AI API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/azario0/csv-chat-app.git
    cd csv-chat-app
    ```
    *(Note: Replace `csv-chat-app` with your actual repository name if different)*

2.  **Create and activate a virtual environment:**
    -   **On macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   **On Windows:**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    -   Create a new file named `.env` in the root of the project directory.
    -   Add your Google AI API key to this file:
        ```ini
        # .env
        GOOGLE_API_KEY="YOUR_GOOGLE_AI_API_KEY_HERE"
        ```
    -   **Important:** The `.gitignore` file is already configured to ignore `.env`, so your secret key will not be committed to Git.

### Running the Application

1.  **Start the Flask server:**
    ```bash
    flask run
    ```

2.  **Access the web app:**
    -   Open your web browser and navigate to `http://127.0.0.1:5000`.

---

## 📋 How to Use

1.  **Upload File**: Click the "Choose File" button and select a `.csv` or `.xlsx` file from your computer.
2.  **Start Chatting**: Once the file is uploaded, a data preview will appear, and you can start asking questions in the chatbox.
3.  **Ask Questions**: Type your question and press "Ask". For example:
    -   `What is the average rating per device_type?`
    -   `Give me a pie chart about device_type`
    -   `Which 5 users have the most helpful votes?`
4.  **Reset**: To start over with a new file, simply click the "Reset & Upload New File" button. This will clear the session and delete the old file from the server.

## 📁 Project Structure

```
/csv-chat-app
|
├── static/
│   ├── charts/           # Generated charts are saved here
│   ├── uploads/          # Uploaded CSVs are saved here
│   └── css/style.css     # Custom styles
|
├── templates/
│   └── index.html        # Main HTML template
|
├── .env                  # Stores the secret API key (you create this)
├── .gitignore            # Specifies files for Git to ignore
├── app.py                # Main Flask application logic
└── requirements.txt      # Python dependencies
```

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Created by [azario0](https://github.com/azario0). Happy chatting with your data!
```