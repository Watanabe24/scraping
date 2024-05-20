import requests
from bs4 import BeautifulSoup
import time

# Base URL settings
base_url = 'https://employment.en-japan.com'
search_base_url = f'{base_url}/a/kanto/search/search_list/'

# Function to scrape job listings
def scrape_job_listings(start_page, end_page):
    seen_jobs = set()  # Set to store seen job URLs or titles
    
    # Keywords to filter out specific industries
    industry_keywords = ['銀行', '不動産', '介護', '映画', '建築', 'コンサルタント', '店長', 'リフォーム',
                         'コールセンター', '建物', 'パン', 'マンション', '飲料', '福祉', 'ルーム', '料理長',
                         'タクシー', '看護', '倉庫', 'ドライバー', '戦略', 'コンサル', '教師', '賃貸', '納棺',
                         '提案', '学校', '給食', '製造', '写真', '事務', '保育', '人材', '土地', '葬祭', '住宅',
                         '清掃', '企画', '受付']
    
    for page_num in range(start_page, end_page + 1):
        # Correctly formatted f-string
        url = f"{search_base_url}?areaid=23_24_22_21_50&occupation=109000_204510_209000_256015_259000_300000_359000_559000"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finding all 'a' tags with href attributes
        a_tags = soup.find_all('a', href=True)
        for a in a_tags:
            link = a['href']
            if not link.startswith('http'):
                link = f"{base_url}{link}"
            # Filtering links that start with the base URL and contain 'desc_'
            if link.startswith(f"{base_url}/desc_"):
                h2 = a.find_previous("h2")
                if h2:
                    h2_text = h2.text.strip()
                    # Check if job has already been seen and not in excluded industries
                    if h2_text not in seen_jobs and not any(keyword in h2_text for keyword in industry_keywords):
                        seen_jobs.add(h2_text)  # Mark job as seen
                        print(f"Page {page_num}: Job: {h2_text}")
                        print(f"Link: {link}\n")

        # Sleep to avoid overloading the server
        time.sleep(1)

# Example usage
scrape_job_listings(1, 15)  # Scrape pages 1 through 15
