from bs4 import BeautifulSoup
from selenium import webdriver


def get_known_issues(driver: webdriver, kb: str) -> [(str, str)]:
    url = f'https://support.microsoft.com/en-us/help/{kb}'
    driver.get(url)

    result = []

    # find table in the page
    tbodies = driver.find_elements_by_tag_name('tbody')
    for tbody in tbodies:
        soup = BeautifulSoup(tbody.get_attribute('innerHTML'), 'html.parser')

        # Check the header of the table.
        header = soup.find('tr').find('td')
        if header.text != 'Symptom':
            continue

        # Extract symptom and workaround from each row of the table.
        for row in soup.find_all('tr')[1:]:
            cells = row.find_all('td')
            result.append((cells[0].get_text(), cells[1].get_text()))

    return result


if __name__ == "__main__":
    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    known_issues = get_known_issues(driver, '4559003')

    driver.quit()

    for item in known_issues:
        print('--- Symptom ---')
        print(item[0])
        print('--- Workaround ---')
        print(item[1])
