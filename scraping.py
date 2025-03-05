from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium with headless mode
options = Options()
options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Base URL for Yahoo Finance with pagination
base_url = "https://finance.yahoo.com/markets/stocks/most-active/?start={}&count=25"

# List to store extracted symbol-company pairs
symbol_company_list = []

# Set max number of pages to scrape (adjust as needed)
max_pages = 16 # Scrapes 5 pages (change this for more pages)

for page in range(0, max_pages * 25, 25):  # Pagination: start=0,25,50...
    url = base_url.format(page)
    driver.get(url)

    # Wait for table rows to load
    wait = WebDriverWait(driver, 10)
    table_rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tr')))

    for row in table_rows:
        try:
            # Extract symbol
            symbol_element = row.find_element(By.CLASS_NAME, "yf-d2uhxq")
            symbol = symbol_element.text.strip()

            # Extract company name
            company_element = row.find_element(By.CLASS_NAME, "yf-362rys")
            company = company_element.text.strip()

            # Append to list
            symbol_company_list.append((symbol, company))
        except Exception as e:
            continue  # Skip rows that don't contain both elements
        print(symbol, company)

# Print all extracted symbols and companies
print(symbol_company_list)

# Close the browser
driver.quit()
