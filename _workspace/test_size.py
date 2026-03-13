from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # Desktop wide
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/index.html")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/size_1440.png")
    print("1. 1440x900 captured")

    # Desktop standard
    page.set_viewport_size({"width": 1200, "height": 800})
    page.reload()
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/size_1200.png")
    print("2. 1200x800 captured")

    # Flip to content page
    page.evaluate("document.getElementById('zoneRight').click()")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/size_content.png")
    print("3. Content page captured")

    browser.close()
    print("Done!")
