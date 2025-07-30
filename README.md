
📚 Library Management System (Python CLI App)

A full-featured command-line Library Management System built using Python. This system allows for easy tracking of books, readers, issuing/returning operations, membership plans, payments, and fine management — all backed by JSON for persistent data storage.

---

🚀 Features

- ✅ Add, update, delete, and search books by title, author, genre, or language  
- 👤 Reader registration/login using phone number  
- 📘 Issue and return books with due dates and fine calculation  
- 🏷️ Membership system with different plans: Basic, Premium, and VIP  
- 💳 Payment handling for book purchase, membership, and fines  
- 📄 Persistent data storage using JSON (no database required)  
- 🔒 Input validation for phone numbers, card details, CVV, expiry dates using regex  
- 📊 Reader profile with history and currently issued books  
- 🔁 Unique ID generation for books, readers, issues, payments

---

🧰 Tech Stack

- **Language**: Python 3  
- **Concepts**: OOP, File I/O, Exception Handling, DateTime, Regex  
- **Libraries**:  
  - `uuid` – for generating unique IDs  
  - `isbnlib` – for validating/generated ISBN numbers  
  - `json` – for structured file-based data persistence  
  - `re`, `datetime`, `random`, `os`

---

📂 Project Structure

```
📁 Library_Management/
├── Library_Management.py          # Main app logic
├── Books_Library.json             # All book records
├── Lib_reader.json                # Registered reader profiles
├── issued_books.json              # Book issue/return records
├── memberships.json               # Membership data
├── payments.json                  # Payment transaction records
```

---

⚙️ How to Run

```bash
git clone https://github.com/your-username/Library-Management-System.git
cd Library-Management-System
python Library_Management.py
```

⚠ Requires Python 3.x installed on your system

---

📌 Future Enhancements

- GUI version using Tkinter or PyQt  
- Export reports in Excel/PDF format  
- Integrate SQLite or PostgreSQL for database support  
- Admin login and dashboard  
- Email alerts for due books and payments

---

🙋‍♂️ Author
**Vishal Patil**
