import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&l=South+Korea"


def get_last_pages():
    html = requests.get(URL)
    #html 전부 가져옴
    soup = BeautifulSoup(html.text, "html.parser")
    #html중에서 class 명이 pagination인 것만
    pagination = soup.find("div", {"class": "s-pagination"})
    #print(pagination)
    if pagination is None:
      return 1
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(link.find("span").string)
        #pages.append(int(link.string))
    #마지막 페이지
    max_page = int(pages[-1])
    print(max_page)
    return max_page


def extract_job(job_info):
    title = job_info.find("h2", {"class": "fs-body3 mb4 fc-black-800"}).string
    #print(title)
    company = job_info.find("h3", {
        "class": "fc-black-700 fs-body1 mb4"
    }).find("span").string
    if company is not None:
        company = company.strip()
    #print(company)
    location = job_info.find("h3", {
        "class": "fc-black-700 fs-body1 mb4"
    }).find("span", {
        "class": "fc-black-500"
    }).string
    location = location.strip()
    #print(location)
    #print(job_info)
    job_id = job_info["data-jobid"]
    #print(job_id)
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"scrapping page {page+1}")
        html = requests.get(f"{URL}&sort=i&pg={page+1}")
        soup = BeautifulSoup(html.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
          if result is None:
            return jobs
          job = extract_job(result)
          jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_pages()
    jobs = extract_jobs(last_page)
    return jobs
