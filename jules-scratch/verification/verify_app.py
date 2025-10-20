import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Navigate to the local HTML file
        file_path = os.path.abspath('amway_business_planner_final_tree.html')
        await page.goto(f'file://{file_path}')

        # --- VERIFY VISUAL BUILDER ---
        # Add two child nodes to the root. Use force=True because the zoom controls can overlap.
        await page.locator('.org-node-btn.add').first.click(force=True)
        await page.wait_for_timeout(300)
        await page.locator('.org-node-btn.add').first.click(force=True)
        await page.wait_for_timeout(300)

        # Explicitly wait for the first child node (the second .org-node overall) to appear
        first_child_node = page.locator('.org-node').nth(1)
        await first_child_node.wait_for(state='visible')

        # Now click the "add" button on that specific child node
        await first_child_node.locator('.org-node-btn.add').click()
        await page.wait_for_timeout(300)

        # Take a screenshot of the final visual builder state
        await page.screenshot(path='jules-scratch/verification/01_visual_builder.png')

        # --- VERIFY OTHER TABS ---
        # Set up a dialog handler BEFORE triggering the alert
        page.on("dialog", lambda dialog: dialog.accept())

        # Push the current structure to Multi-Month Planning
        await page.click('button:has-text("Push to Multi-Month")')
        await page.wait_for_timeout(200)

        # Switch to Multi-Month Planning tab and take a screenshot
        await page.click('button[data-tab="multimonth"]')
        await page.wait_for_timeout(500)
        await page.screenshot(path='jules-scratch/verification/02_multimonth_planning.png')

        # Switch to Analytics and take a screenshot
        await page.click('button[data-tab="analytics"]')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='jules-scratch/verification/03_analytics.png')

        # Switch to Incentives and take a screenshot
        await page.click('button[data-tab="incentives"]')
        await page.wait_for_timeout(500)
        await page.screenshot(path='jules-scratch/verification/04_incentives.png')

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
