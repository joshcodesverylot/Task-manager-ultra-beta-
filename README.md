# AI-Powered Task Manger

A desktop task management application built with Python and Tkinter.It features real-time AI categorization to automatically tag tasks based on content.

Features-
Smart Categorization:** Uses Google Gemini API to auto-tag tasks (e.g. "Buy Milk" -> "Groceries")
Multi-Threaded UI:** Implements threading to keep the interface responsive when API calling.
Data Persistance:** Saves and loads tasks instantly using JSON.
Task Management:** Create, Read, Update, and Delete (CRUD) functionality with Priority sorting.

Technologies Used-
Language:** Python 3.10+
GUI:** Tkinter (Custom Treeview implementation)
AI:* Google Gemini API
Concepts:** Multi-threading, MVC Architecture, JSON Serialization.

## 📦 How to Run
1. Clone the repository.
2. Install dependencies: `pip install google-generativeai`
3. Add your API Key in `ai_helper.py`.
4. Run the app: `python app_ui.py`
