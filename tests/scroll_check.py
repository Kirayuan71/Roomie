"""Run a Streamlit server on port 8501, then: python tests/scroll_check.py.
Requires Playwright and Chromium (CHROMIUM_PATH may override the executable).
"""
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), headless=True, args=['--no-sandbox'])
    page = browser.new_page()
    page.goto(os.environ.get('ROOMIE_TEST_URL', 'http://localhost:8501'))
    page.locator('iframe').wait_for()
    for width, height in [(1440, 900), (390, 844), (390, 500), (844, 390)]:
        page.set_viewport_size({'width': width, 'height': height})
        frame = next(f for f in page.frames if '/component/' in f.url)
        frame.get_by_text('小家日历', exact=True).wait_for()
        page.wait_for_timeout(250)
        bounds = page.locator('iframe').bounding_box()
        assert bounds and abs(bounds['height'] - height) < 2, bounds
        assert abs(bounds['y']) < 2, bounds
        frame.evaluate("document.querySelector('.app').scrollTo(0, 0)")
        page.mouse.move(width * .7, height * .7)
        page.mouse.wheel(0, 30000)
        page.wait_for_timeout(350)
        position = frame.evaluate('''() => {
            const el=document.querySelector('.app');
            const footer=document.querySelector('footer').getBoundingClientRect();
            return {remaining:el.scrollHeight-el.scrollTop-innerHeight, bottom:footer.bottom, top:footer.top, height:innerHeight};
        }''')
        assert position['remaining'] < 2, position
        assert position['bottom'] <= height and position['top'] >= 0, position
        if width <= 650:
            assert position['bottom'] <= frame.locator('.mobile-nav').bounding_box()['y'], position
        assert page.locator('[data-testid="stMain"]').evaluate('(el)=>el.scrollTop') == 0
        assert frame.evaluate('document.documentElement.scrollWidth <= innerWidth')
        print(f'PASS {width}x{height}: single scroll area, footer reachable, host stable')
    # A longer board must scroll inside the frame without changing its height.
    frame.evaluate('''()=>{const s=JSON.parse(localStorage.getItem('roomie-v1'));s.messages=Array.from({length:30},(_,i)=>({...s.messages[0],id:'scroll-'+i}));localStorage.setItem('roomie-v1',JSON.stringify(s));location.reload()}''')
    frame.get_by_text('小家日历', exact=True).wait_for()
    page.wait_for_timeout(300)
    before = page.locator('iframe').bounding_box()['height']
    frame.evaluate("document.querySelector('.app').scrollTo(0,document.querySelector('.app').scrollHeight)")
    page.wait_for_timeout(200)
    assert page.locator('iframe').bounding_box()['height'] == before
    assert frame.evaluate("document.querySelector('.app').scrollHeight-document.querySelector('.app').scrollTop-innerHeight") < 2
    print('PASS long message board: stable iframe height and reachable bottom')
    browser.close()
