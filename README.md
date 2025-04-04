# Iden Challenge

This project automates the Iden HQ challenge using Playwright (sync) in Python. It extracts product data from a dynamic web page and saves it in JSON format. It also manages session data for efficient logins.

---

## 📁 Project Structure

```
.
├── data
│   ├── products.json
│   └── session.json
├── pyproject.toml
├── README.md
├── requirements-dev.lock
├── requirements.lock
├── scripts
│   ├── exceptions.py
│   ├── iden_challenge.py
│   └── __pycache__
│       └── exceptions.cpython-312.pyc
└── src
    └── iden_playwright
        └── __init__.py
```

---

## 🧰 Technologies Used

- [Playwright](https://playwright.dev/python/) (sync)
- Python 3.12+
- Rye (for dependency and environment management)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/hemanth-kumar-j/iden-challenge.git
cd iden-challenge
```

### 2. Install Rye (if not already installed)
Visit [https://rye-up.com](https://rye-up.com) for installation instructions.

### 3. Setup Environment
```bash
rye sync
rye run playwright install
```

### 4. Run the Script (Sync Version)
```bash
python scripts/iden_challenge.py
```

---

## 🧪 Features

- ✅ Automatic login with session persistence
- ✅ Detects login success popup using custom exceptions
- ✅ Step-by-step navigation to reveal product data
- ✅ Dynamic scrolling and data extraction
- ✅ Save data in `products.json`
- ✅ Handles failures with meaningful error messages

---

## ⚙️ Configuration

Session and product data are saved inside the `data/` folder:

- `session.json`: stores sessionStorage for reuse
- `products.json`: stores extracted product info

To test the login process again, delete the `data/session.json` file before running the script:
```bash
rm data/session.json
python scripts/iden_challenge.py
```

---