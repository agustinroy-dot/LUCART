from playwright.sync_api import sync_playwright, expect
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # Go to login
        page.goto("http://127.0.0.1:5000/auth/login")

        # Fill login form
        if page.locator("input[name='username']").count() > 0:
            page.fill("input[name='username']", "admin")
            page.fill("input[name='password']", "admin")
            page.click("button[type='submit'], input[type='submit']")
            page.wait_for_url("http://127.0.0.1:5000/")

        # Go to Orders page
        page.goto("http://127.0.0.1:5000/orders/")

        # Click on the first "View" button
        # Wait for table
        page.wait_for_selector("table")

        # Click View on first row
        with page.expect_navigation():
            page.locator("a.btn-secondary").first.click()

        # Expect Order details
        expect(page.locator("h1.page-title")).to_contain_text("Order #")

        # Expect "Material Usage Tracking" section
        expect(page.locator("h3", has_text="Material Usage Tracking")).to_be_visible()

        # Take screenshot
        if not os.path.exists("verification"):
            os.makedirs("verification")
        page.screenshot(path="verification/verification.png")
        print("Screenshot saved to verification/verification.png")

    except Exception as e:
        print(f"Error: {e}")
        # Take screenshot on error
        if not os.path.exists("verification"):
            os.makedirs("verification")
        page.screenshot(path="verification/error.png")
        raise e
    finally:
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
