
from playwright.sync_api import sync_playwright, expect
import time

def run():
    print("Starting Playwright verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Login
            print("Navigating to login...")
            page.goto("http://127.0.0.1:5000/auth/login")
            page.fill("input[name='username']", "admin")
            page.fill("input[name='password']", "admin")

            # Click submit button
            if page.locator("input[type='submit']").count() > 0:
                page.click("input[type='submit']")
            else:
                page.click("button[type='submit']")

            print("Logged in. Waiting for dashboard...")
            page.wait_for_url("http://127.0.0.1:5000/")
            print("Dashboard loaded.")

            # Go to orders index
            print("Navigating to orders...")
            page.goto("http://127.0.0.1:5000/orders/")

            # Click first order link
            print("Looking for order link...")
            first_order_link = page.locator("table tbody tr:first-child td:first-child a")
            if first_order_link.count() > 0:
                first_order_link.click()
                print("Clicked order link.")
            else:
                print("No orders found in table. Creating a new one...")
                page.goto("http://127.0.0.1:5000/orders/new")
                # Fill new order form
                page.select_option("select[name='customer_id']", index=1)
                page.fill("input[name='description']", "Test Order Playwright")
                page.fill("input[name='price']", "100")
                page.fill("input[name='date_due']", "2023-12-31")
                # Submit
                if page.locator("input[type='submit']").count() > 0:
                    page.click("input[type='submit']")
                else:
                    page.click("button[type='submit']")
                print("Created new order.")

            # Verify view page loaded
            print("Waiting for view page...")
            page.wait_for_selector("h1.page-title")
            expect(page.locator("h1.page-title")).to_contain_text("Order #")

            # Take screenshot
            print("Taking screenshot...")
            page.screenshot(path="verification/order_view.png", full_page=True)
            print("Screenshot saved to verification/order_view.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run()
