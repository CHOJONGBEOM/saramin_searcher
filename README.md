
![Uploading 사람인 스크래퍼 사용예시.gif…]()





# 사람인 스크래퍼

이 프로젝트는 사람인 웹사이트에서 직무 정보를 스크래핑하는 Python으로 제작한 윈도우 애플리케이션입니다. 사용자는 원하는 키워드를 입력하여 관련된 직무 정보를 CSV 파일로 저장할 수 있습니다.

## 기능
- 특정 키워드에 대한 직무 정보 검색
- 검색 결과를 CSV 파일로 저장
- PyQt5를 사용한 GUI 제공

## 요구 사항

이 애플리케이션을 실행하기 위해서는 다음의 Python 라이브러리가 필요합니다:

- PyQt5
- BeautifulSoup4
- Playwright

## 설치 방법

다음 단계를 따라 이 애플리케이션을 설치하고 실행하세요.

### 1. Python 설치 확인

1. **Python 설치 확인**:
   - Windows에서 명령 프롬프트를 열고 다음 명령어를 입력하여 Python이 설치되어 있는지 확인합니다.
     ```cmd
     python --version
     ```
   - Python 버전이 출력되면 설치가 완료된 것입니다. 그렇지 않다면 [Python 공식 웹사이트](https://www.python.org/downloads/)에서 다운로드하여 설치하세요.

### 2. 필요한 라이브러리 설치

1. **명령 프롬프트 열기**:
   - Windows 키를 누르고 "cmd"를 입력한 후 Enter 키를 눌러 명령 프롬프트를 엽니다.

2. **PyQt5 및 Playwright 설치**:
   - 다음 명령어를 입력하여 PyQt5와 Playwright를 설치합니다.
     ```cmd
     pip install PyQt5 beautifulsoup4 playwright
     ```

3. **Playwright 브라우저 설치**:
   - Playwright가 사용할 브라우저를 설치합니다.
     ```cmd
     playwright install
     ```

### 3. 소스 코드 다운로드

1. **소스 코드 다운로드**:
   - GitHub 또는 다른 소스에서 `saramin_search.py` 파일을 다운로드합니다.

### 4. 실행 파일 생성

이 프로그램을 실행 가능한 `.exe` 파일로 만들기 위해, 다음 단계를 따르세요.

1. **필요한 라이브러리 설치**:
   - 다음 명령어를 입력하여 라이브러리를 설치합니다
     ```cmd
     pip install PyQt5 beautifulsoup4 playwright pyinstaller
     ```

2. **Playwright 브라우저 설치**:
     ```cmd
     playwright install chromium
     ```
3. **Playwright 브라우저를 실행 파일에 포함시키기 위해 환경 변수를 설정합니다.**:
     ```cmd
     set PLAYWRIGHT_BROWSERS_PATH=0
     ```
4. **PyInstaller로 실행 파일 생성**:
   - 코드가 저장된 디렉토리로 이동한 후 다음 명령어를 실행합니다.
     ```cmd
     pyinstaller --onefile --windowed --collect-all playwright saramin_search.py
     ```
5. **실행 파일 실행 (선택 사항)**:
   - `dist` 폴더 안에 있는 `saramin_search.exe` 파일을 더블 클릭하여 프로그램을 실행합니다.
   - 1. GUI 창이 열리면, 검색어를 입력하고 "검색" 버튼을 클릭합니다.
     2. 검색이 완료되면 결과가 `saramin_search_results.csv` 파일로 저장됩니다.




  
