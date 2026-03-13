from playwright.sync_api import sync_playwright
import time

BASE = "http://localhost:8080"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1200, "height": 800})

    page.goto(f"{BASE}/index.html")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Screenshot 1: Initial state
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_01_initial.png")
    print("1. Initial state captured")

    # Flip forward
    page.evaluate("document.getElementById('zoneRight').click()")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_02_after_first_flip.png")
    print("2. After first flip captured")

    # Flip forward again
    page.evaluate("document.getElementById('zoneRight').click()")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_03_after_second_flip.png")
    print("3. After second flip captured")

    # Flip back
    page.evaluate("document.getElementById('zoneLeft').click()")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_04_after_back_flip.png")
    print("4. After back flip captured")

    # Keyboard right
    page.keyboard.press("ArrowRight")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_05_keyboard_right.png")
    print("5. Keyboard right captured")

    # Jump to end
    page.keyboard.press("End")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_06_end.png")
    print("6. End page captured")

    # Mobile viewport
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{BASE}/index.html")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_07_mobile.png")
    print("7. Mobile initial captured")

    # Mobile flip
    page.evaluate("document.getElementById('zoneRight').click()")
    time.sleep(1.5)
    page.screenshot(path="/Users/robin/Downloads/claude-code-starter/_workspace/flip_08_mobile_flip.png")
    print("8. Mobile flip captured")

    browser.close()
    print("\nAll screenshots captured successfully!")
