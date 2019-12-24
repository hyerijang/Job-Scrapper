import requests
from bs4 import BeautifulSoup

LIMIT = 50

URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"


def get_last_pages():
    html = requests.get(URL)
    #html 전부 가져옴
    soup = BeautifulSoup(html.text, "html.parser")
    #html중에서 class 명이 pagination인 것만
    pagination = soup.find("div", {"class": "pagination"})
    #list of links
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    #마지막 페이지
    max_page = pages[-1]
    return max_page


def extract_job(job_info):
    title = job_info.find("div", {"class": "title"}).find("a")["title"]
    #company는 soup
    company = job_info.find("span", {"class": "company"})
    #soup로 찾은 결과 company_ancher에 담음
    company_ancher = company.find("a")
    #company에 담긴 기존 soup 없애고 이름만 담음
    if company_ancher is not None:
        company = str(company_ancher.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = job_info.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = job_info["data-jk"]
    return {
        'title':
        title,
        'company':
        company,
        'location':
        location,
        'link':
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_pages()
    jobs = extract_jobs(last_page)
    return jobs
