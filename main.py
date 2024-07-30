
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36

def get_job_listings(keywords, location):
    job_listings = []
    headers = {
        "User-Agnet": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    search_keywords = " OR ".join(keywords)
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_keywords}&location={location}&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        job_cards = soup.find_all('li', class_="result-card job-result-card result-card--with-hover-state")
        for job in job_cards:
            title =  job.find('h3', class_="result-card__title").text.strip()
            company_name = job.find('h4', class_="result-card__subtitle").text.strip()
            posted_date = job.find('time').text.strip()
            location = job.find('span', class_="result-card__location").text.strip()

            if any(keyword.lower() in title.lower() for keyword in keywords):
                job_listings.append({
                    'Title': title,
                    'Company Name': company_name,
                    'Location': location,
                    'Posted Date': posted_date
                })

    return job_listings

def save_to_csv(job_listings, filename):
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index = False)

keywords = ["analytics", "analysis"]
location = "Dhaka"
job_listings = get_job_listings(keywords, location)
save_to_csv(job_listings, "linkedin_search.csv")
