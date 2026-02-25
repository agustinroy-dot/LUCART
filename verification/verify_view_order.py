import os
from playwright.sync_api import sync_playwright

def verify(page):
    # 1. Login
    print("Navigating to login...")
    page.goto("http://127.0.0.1:5000/auth/login")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "admin")

    # Click login - assuming standard structure
    print("Logging in...")
    page.click("input[type='submit']")

    # 2. Go to order view
    print("Navigating to order 1...")
    page.goto("http://127.0.0.1:5000/orders/1")

    # 3. Check for Add Material form
    print("Checking for Add Material form...")
    fieldset = page.locator("fieldset:has(legend:has-text('Add Material'))")
    fieldset.wait_for()
    fieldset.scroll_into_view_if_needed()

    # 4. Take screenshot of the relevant area
    if not os.path.exists("verification"):
        os.makedirs("verification")

    page.screenshot(path="verification/order_view_full.png", full_page=True)
    fieldset.screenshot(path="verification/order_view_form.png")
    print("Screenshots saved to verification/")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            verify(page)
        except Exception as e:
            print(f"Error: {e}")
            if not os.path.exists("verification"):
                os.makedirs("verification")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()
