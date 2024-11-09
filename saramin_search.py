import sys
import os
import csv
import time
import traceback
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def exception_hook(exctype, value, tb):
    print(f"예외 발생: {exctype.__name__}: {value}")
    print("".join(traceback.format_tb(tb)))
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = exception_hook

class ScraperThread(QThread):
    update_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(list)

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                page.goto("https://www.saramin.co.kr/zf_user/")
                time.sleep(5)
                page.click("a.depth1")
                time.sleep(5)
                page.locator("label[for='loc_mcd_101000']").click()
                time.sleep(2)
                page.click("button.btn_search")
                time.sleep(5)
                page.get_by_placeholder("직무, 회사, 지역, 키워드로 검색해보세요").fill(self.keyword)
                time.sleep(5)
                page.keyboard.down("Enter")
                time.sleep(5)
                page.get_by_role("button", name="경력 선택").click()
                time.sleep(5)
                page.locator("#btn_check_career_over0").click()
                time.sleep(5)
                page.get_by_role("button", name="경력 1년 이하").click()
                time.sleep(5)
                page.get_by_role("button", name="학력 선택").click()
                time.sleep(5)
                page.locator("#btn_check_edu_3").click()
                time.sleep(5)
                page.get_by_role("button", name="대학교(4년) 졸업").click()
                time.sleep(5)
                page.click("button#search_btn")
                time.sleep(5)

                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                pagination = soup.find("div", class_="pagination")
                
                last_page = 1
                if pagination:
                    pages = pagination.find_all("span")
                    for page_span in pages:
                        if page_span.text.isdigit():
                            last_page = max(last_page, int(page_span.text))
                
                self.update_signal.emit(f"총 {last_page}페이지를 스크래핑합니다.")

                jobs_db = []
                for x in range(1, last_page + 1):
                    if x > 1:
                        page.click(f"a[page='{x}']")
                        time.sleep(7)
                    
                    content = page.content()
                    soup = BeautifulSoup(content, "html.parser")
                    jobs = soup.find_all("div", class_="item_recruit")
                    
                    for job in jobs:
                        title = job.find('a')['title']
                        company_name = job.find('a').text.strip()
                        link = f"https://saramin.co.kr{job.find('a')['href']}"
                        date = f"{job.find('span', class_='date').text}까지"
                        job_info = {
                            "title": title,
                            "company_name": company_name,
                            "link": link,
                            "마감날짜": date
                        }
                        jobs_db.append(job_info)
                    
                    self.update_signal.emit(f"{x}/{last_page} 페이지 완료")

                browser.close()

                self.finished_signal.emit(jobs_db)
        except Exception as e:
            self.update_signal.emit(f"오류 발생: {str(e)}")
            print(traceback.format_exc())

class SaraminSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('사람인 직무 검색')
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.keyword_input = QLineEdit()
        search_button = QPushButton('검색')
        search_button.clicked.connect(self.start_search)
        input_layout.addWidget(QLabel('검색어:'))
        input_layout.addWidget(self.keyword_input)
        input_layout.addWidget(search_button)

        layout.addLayout(input_layout)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def start_search(self):
        keyword = self.keyword_input.text()
        if not keyword:
            self.result_text.setText("검색어를 입력해주세요.")
            return

        self.result_text.clear()
        self.result_text.append(f"'{keyword}' 검색을 시작합니다...")
        
        self.scraper_thread = ScraperThread(keyword)
        self.scraper_thread.update_signal.connect(self.update_progress)
        self.scraper_thread.finished_signal.connect(self.save_results)
        self.scraper_thread.start()

    def update_progress(self, message):
        self.result_text.append(message)

    def save_results(self, jobs_db):
        file_name = "saramin_search_results.csv"
        
        try:
            with open(file_name, "w", encoding="utf-8", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["title", "company_name", "link", "마감날짜"])
                writer.writeheader()
                writer.writerows(jobs_db)

            self.result_text.append(f"\n검색 완료! 결과가 다음 위치에 저장되었습니다:\n{os.path.abspath(file_name)}")
        except Exception as e:
            self.result_text.append(f"\n결과 저장 중 오류 발생: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SaraminSearchApp()
    ex.show()
    sys.exit(app.exec_())