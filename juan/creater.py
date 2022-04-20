from playwright.sync_api import Playwright, sync_playwright, expect
import bs4, time, datetime

def addtofile(path, data):
    with open(path, 'a', encoding='UTF-8') as f:
        f.write(data)
        f.close()

def access(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    # Open new page
    while True:
        print("Exploring")
        page = context.new_page()
        # Go to https://www.zxx.edu.cn/
        page.goto("https://www.zxx.edu.cn/")
        page.wait_for_load_state('networkidle')
        html = page.content()
        # Close page
        page.close()
        # ---------------------
        context.close()
        browser.close()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        text = soup.text
        p_f = text.index("做眼保健操今天已有")
        p_e = text.index("人与你一起学习")
        t_f = text.index("你们共浏览了")
        t_e = text.index("次。主办")
        person = text[p_f+9:p_e]
        person = int(person.replace(",",""))
        times = text[t_f+6:t_e]
        times = int(times.replace(",",""))
        print("Person: " + str(person))
        print("Times: " + str(times))
        total = [person, times, datetime.datetime.now().strftime('%Y-%m-%d')]
        addtofile("data.txt",str(total) + "\n")
        print("Data added completed")
        time.sleep(300)


with sync_playwright() as playwright:
    access(playwright)
