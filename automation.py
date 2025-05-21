import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 1. LOGIN
        await page.goto("http://localhost:5000/login")
        await page.fill('input[name="username"]', "admin")  # CHANGE THIS
        await page.fill('input[name="password"]', "admin123")  # CHANGE THIS
        await page.click('button[type="submit"]')
        await page.wait_for_url("**/dashboard")

        # 2. CREATE COUNTRY
        await page.goto("http://localhost:5000/country")
        country_name = "Australia"
        await page.fill('input[name="country_name"]', country_name)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)  # Wait for reload

        # 3. CREATE STATE
        await page.goto("http://localhost:5000/state")
        state_name = "AutoState"
        await page.select_option('select[name="country_id"]', label=country_name)
        await page.fill('input[name="state_name"]', state_name)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 4. CREATE CITY
        await page.goto("http://localhost:5000/city")
        city_name = "AutoCity"
        await page.fill('input[name="city_name"]', city_name)
        await page.wait_for_selector('select[name="state_id"]')
        await page.select_option('select[name="state_id"]', label="AutoState (AutoCountry)")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        city_id = city_name  # Use city_name as the label for select_option

        # 5. CREATE CUSTOMER
        await page.goto("http://localhost:5000/customer")
        await page.fill('input[name="customer_name"]', "AutoCustomer")
        await page.fill('input[name="contact_person"]', "ContactPerson")
        await page.fill('input[name="contact_number"]', "1234567890")
        await page.fill('input[name="email"]', "auto@customer.com")
        await page.fill('textarea[name="address"]', "Automation Address")
        await page.select_option('select[name="country_id"]', label=country_name)
        await page.select_option('select[name="state_id"]', label=state_name)
        await page.select_option('select[name="city_id"]', label=city_id)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 6. CREATE TRANSPORTER
        await page.goto("http://localhost:5000/transporter")
        await page.fill('input[name="transporter_name"]', "AutoTransporter")
        await page.fill('input[name="contact_person"]', "TransportContact")
        await page.fill('input[name="contact_number"]', "9876543210")
        await page.fill('input[name="email"]', "auto@transporter.com")
        await page.fill('textarea[name="address"]', "Transporter Address")
        await page.select_option('select[name="country_id"]', label=country_name)
        await page.select_option('select[name="state_id"]', label=state_name)
        await page.select_option('select[name="city_id"]', label=city_id)
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 7. CREATE ITEM
        await page.goto("http://localhost:5000/item")
        await page.fill('input[name="item_name"]', "AutoItem")
        await page.fill('input[name="item_code"]', "AI001")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 8. CREATE JOB ORDER
        await page.goto("http://localhost:5000/job_order")
        await page.fill('input[name="job_order_number"]', "JO-AUTO-001")
        await page.select_option('select[name="customer_id"]', label="AutoCustomer")
        await page.select_option('select[name="transporter_id"]', label="AutoTransporter")
        await page.select_option('select[name="origin_city_id"]', label=city_id)
        await page.select_option('select[name="destination_city_id"]', label=city_id)
        await page.fill('input[name="order_date"]', "2025-05-21")
        
        await page.select_option('select[name="item_id"]', label="AutoItem")
        await page.fill('input[name="quantity"]', "1")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 9. PICKUP ACCEPTANCE
        await page.goto("http://localhost:5000/pickup_acceptance")
        await page.select_option('select[name="job_order_id"]', label="JO0001")
        await page.fill('input[name="pickup_date"]', "2025-05-21")
        await page.fill('input[name="accepted_by"]', "Automation")
        await page.fill('textarea[name="remarks"]', "Automated pickup")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 10. ADD POD
        await page.goto("http://localhost:5000/pod")
        await page.select_option('select[name="job_order_id"]', label="JO0001")
        await page.fill('input[name="delivery_date"]', "2025-05-21")
        await page.fill('input[name="received_by"]', "Automation")
        await page.fill('textarea[name="remarks"]', "Automated POD")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)

        # 11. VERIFY IN MIS POD
        await page.goto("http://localhost:5000/mis/pod")
        await page.wait_for_selector("table")
        assert await page.is_visible("text=JO0001"), "POD not found in MIS POD!"
        print("Automation completed successfully!")

        await browser.close()

asyncio.run(main())