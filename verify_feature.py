from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Login
    print("Navigating to login...")
    page.goto("http://localhost:5000/auth/login")
    page.fill("input[name='username']", "admin")
    page.fill("input[name='password']", "admin")
    page.click("input[type='submit']")

    # Go to order 1
    print("Navigating to order view...")
    page.goto("http://localhost:5000/orders/1")

    # Wait for content
    page.wait_for_selector("h1.page-title")

    # Verify Add Material form is present
    page.wait_for_selector("text=Add Material")

    # Screenshot
    print("Taking screenshot...")
    page.screenshot(path="verification_order.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
