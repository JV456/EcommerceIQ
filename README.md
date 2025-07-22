# EcommerceIQ: AI Agent to Answer E-commerce Data Questions

**EcommerceIQ** is an intelligent AI-powered agent designed to answer your questions about e-commerce data. By leveraging natural language processing, this tool allows you to query your sales data in a conversational way, eliminating the need for complex SQL queries. Just ask a question like "What were the total sales last month?" or "Who are my top 10 customers by purchase value?" and get instant answers.

This project uses a Python backend and can connect to either a **SQLite database** or a **MySQL database** to manage and analyze sales information.

---

## ✨ Features

-   **Natural Language Queries**: Ask questions about your data in plain English.
-   **Sales Data Analysis**: Get insights into sales trends, customer behavior, and product performance.
-   **Multiple Database Support**: Connect to the bundled SQLite database or your own external MySQL database.
-   **Extensible**: Easily adaptable to different e-commerce datasets.

---

## 🛠️ How It Works

The application uses a Python script (`app.py`) as its core. It can connect to a database to retrieve information. By default, it uses the provided SQLite database (`sales_analysis.db`), but it can also be configured to connect to your own **MySQL database**. When you ask a question in natural language, the AI agent interprets your query, translates it into a database-readable format, fetches the relevant information, and presents the answer back to you.

---

### Configuration

The application can connect to two types of databases:

1.  **SQLite (Default)**: The repository includes a pre-populated SQLite database `sales_analysis.db`. No configuration is needed to use this.

2.  **MySQL (Optional)**: To connect to your own MySQL database, you need to set the following environment variables. If these are set, the application will automatically connect to your MySQL database instead of SQLite.

    ```
    DB_TYPE=mysql
    MYSQL_HOST=your_mysql_host
    MYSQL_USER=your_mysql_user
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_DB=your_database_name
    ```
    
    You will also need to populate this database with your own e-commerce data.

---

## Usage

1.  **Run the application:**
    ```
    python app.py
    ```
2.  Once the application is running, you can start asking questions in your terminal. The agent will query the configured database (MySQL if variables are set, otherwise SQLite).

### Example Questions:
-   "What is my total sales?"
-   "Calculate the RoAS (Return on Ad Spend)."
-   "Which product had the highest CPC (Cost Per Click)?"

---

## 🧪 Demo

**Demo Link:** https://drive.google.com/file/d/1_FeCfTIcwl-gqAOwq8AiX7zsD8waLF5h/view?usp=sharing

---

If you like this repository, give it a star ⭐!

---






