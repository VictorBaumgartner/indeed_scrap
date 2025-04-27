import requests
from bs4 import BeautifulSoup
import time

def extract(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    url = f'https://fr.indeed.com/jobs?q=Developpeur%20Python&l=Paris&start={page}'
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(r.content, "html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        return None

def transform(soup):
    if not soup:
        return None
    
    jobs = []
    # Updated class name based on Indeed's current structure (as of 2025)
    divs = soup.find_all('div', class_='job_seen_beacon')
    
    for item in divs:
        try:
            # Extract title using more flexible selector
            title_tag = item.find('a', class_='jcs-JobTitle')
            title = title_tag.text.strip() if title_tag else "N/A"
            
            # Extract company with fallback
            company_tag = item.find('span', class_='companyName')
            company = company_tag.text.strip() if company_tag else "N/A"
            
            # Extract location with fallback
            location_tag = item.find('div', class_='companyLocation')
            location = location_tag.text.strip() if location_tag else "N/A"
            
            job = {
                'title': title,
                'company': company,
                'location': location
            }
            jobs.append(job)
            
            # Print for immediate feedback
            print(f"Title: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print("-" * 50)
            
        except AttributeError as e:
            print(f"Error parsing job listing: {e}")
            continue
    
    return jobs

def main():
    all_jobs = []
    for page in range(0, 20, 10):  # Scrape first 2 pages (0, 10)
        print(f"Scraping page {page//10 + 1}...")
        soup = extract(page)
        jobs = transform(soup)
        if jobs:
            all_jobs.extend(jobs)
        time.sleep(1)  # Be polite to the server
    return all_jobs

if __name__ == "__main__":
    jobs = main()
    print(f"Total jobs scraped: {len(jobs)}")