# Iden Challenge

This project automates the Iden HQ challenge using Playwright (sync) in Python. It extracts product data from a dynamic web page and saves it in JSON format. It also manages session data for efficient logins.

---

## Project Structure

```
.
├── data                  # Stores session and extracted product data
│   ├── products.json     # Final scraped product data in JSON format
│   └── session.json      # SessionStorage data for login reuse
├── pyproject.toml        # Project configuration and dependencies managed by Rye
├── README.md             # Project documentation
├── requirements-dev.lock # Development dependency lock file (auto-generated by Rye)
├── requirements.lock     # Production dependency lock file (auto-generated by Rye)
├── scripts
│   ├── exceptions.py     # Custom exception class for popup validations
│   ├── iden_challenge.py # Main script to automate the Iden challenge using sync Playwright
│   └── __pycache__       # Compiled Python bytecode cache
│       └── exceptions.cpython-312.pyc
└── src
    └── iden_playwright
        └── __init__.py   # Package initializer (currently empty)
```

---

## Technologies Used

- [Playwright](https://playwright.dev/python/) (sync)
- Python 3.12+
- Rye (for dependency and environment management)

---

## Getting Started

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

## Features

- Automatic login with session persistence
- Detects login success popup using custom exceptions
- Step-by-step navigation to reveal product data
- Dynamic scrolling and data extraction
- Save data in `products.json`
- Handles failures with meaningful error messages

---

## Configuration

Session and product data are saved inside the `data/` folder:

- `session.json`: stores sessionStorage for reuse
- `products.json`: stores extracted product info

To test the login process again, delete the `data/session.json` file before running the script:
```bash
rm data/session.json
python scripts/iden_challenge.py
```

---