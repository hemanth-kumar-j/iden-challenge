import json
import os
from playwright.sync_api import sync_playwright
from exceptions import PopupNotFoundError

# Define data directory
DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "data")
SESSION_FILE = os.path.join(DATA_DIRECTORY, "session.json")
PRODUCTS_FILE = os.path.join(DATA_DIRECTORY, "products.json")

# Ensure the data directory exists
os.makedirs(DATA_DIRECTORY, exist_ok=True)

# --- Session Handling ---


def save_session(page):
    """Save sessionStorage data to a file."""
    session_data = page.evaluate("JSON.stringify(sessionStorage)")
    with open(SESSION_FILE, "w") as f:
        json.dump({"sessionStorage": json.loads(session_data)}, f, indent=4)
    print("Session data saved!")


def load_session(page):
    """Load sessionStorage data from a file if it exists."""
    with open(SESSION_FILE, "r") as f:
        session_data = json.load(f).get("sessionStorage")
        if session_data:
            page.evaluate(f"Object.assign(sessionStorage, {json.dumps(session_data)})")
            print("Session data loaded!")


# --- Login & Navigation ---


def login(page):
    print("🔑 Logging in...")
    page.fill("#email", "janardhan.hemanth@gmail.com")
    page.fill("#password", "ChCfP0Ks")
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")
    # Check for login success popup
    if not page.locator('//ol//div[contains(text(),"Login successful")]').is_visible():
        raise PopupNotFoundError("Login success popup not found!")

    print("Login successful popup verified!")
    page.wait_for_selector("text=Iden Challenge Instructions", timeout=10000)
    save_session(page)


def navigate_to_product_table(page):
    page.wait_for_selector('//button[text()="Launch Challenge"]').click()

    steps = [
        ("Inventory", "Step 1 completed"),
        ("Catalog", "Step 2 completed"),
        ("Data View", "Step 3 completed"),
        ("View Complete Data", "Table revealed"),
    ]

    for button_text, expected_popup in steps:
        page.wait_for_selector(f'//button[text()="{button_text}"]').click()
        if not page.locator(
            f"//ol//div[contains(text(),'{expected_popup}')]"
        ).is_visible():
            raise PopupNotFoundError(f"'{expected_popup}' popup not found!")
        print(f"{expected_popup} popup verified!")

    page.wait_for_selector("text=Product Inventory")


# --- Data Extraction ---


def get_total_products(page):
    number_span = page.locator('//div[contains(text(),"Showing")]//span[2]')
    return int(number_span.inner_text())


def extract_product_data(page):
    number_of_products = get_total_products(page)
    print(f"Target: {number_of_products} products")

    products = []
    previous_count = 0

    while True:
        rows = page.locator("//tbody/tr").all()
        if not rows:
            page.wait_for_timeout(300)
            continue

        current_count = len(rows)
        new_rows = rows[previous_count:current_count]
        rows_needed = number_of_products - len(products)

        for row in new_rows[:rows_needed]:
            columns = row.locator("td").all()
            product_data = {
                "ID": columns[0].inner_text(),
                "Price": columns[1].inner_text(),
                "Item": columns[2].inner_text(),
                "Material": columns[3].inner_text(),
                "Rating": columns[4].inner_text(),
                "Stock": columns[5].inner_text(),
                "Last Updated": columns[6].inner_text(),
                "Description": columns[7].inner_text(),
                "Color": columns[8].inner_text(),
            }
            products.append(product_data)

        if len(products) >= number_of_products:
            break

        previous_count = current_count
        rows[-1].scroll_into_view_if_needed()
        page.wait_for_timeout(300)

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

    print(f"Captured {len(products)} products to 'data/products.json'")


# --- Main Flow ---


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.goto("https://hiring.idenhq.com/")

        if os.path.exists(SESSION_FILE):
            load_session(page)
            page.reload()
            try:
                page.wait_for_selector("text=Iden Challenge Instructions", timeout=3000)
                print("Already logged in with session!")
            except:
                print("Session invalid, re-authenticating...")
                login(page)
        else:
            print("No session found")
            login(page)

        navigate_to_product_table(page)
        extract_product_data(page)
        browser.close()


if __name__ == "__main__":
    main()
