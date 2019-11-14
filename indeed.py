#find랑 find_all 의 차이
#find_all 은 모든 리스트를 가져오고
#find는 찾은 것중 가장 앞에 것을 가져다줌

import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}&radius=25&start=0"


def get_last_page():
    #웹페이지 정보 싹 가져옴
    result = requests.get(URL)

    #가져온 웹페이지에서 html만 뽑음
    soup = BeautifulSoup(result.text, "html.parser")

    #html에서 내가 원하는 부분인 div에서 class 이름이 pagination인 것만  뽑음
    pagination = soup.find("div", {"class": "pagination"})

    #pagitnation에서 anchor만 뽑음. -> 모든 링크들을 구해다준 것이다. links는 list이다.
    links = pagination.find_all('a')

    #links에서 span만 뽑음
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]

    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company:
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
    else:
        company = None
    company = company.strip()

    location = html.find("span", {"class": "location"}).string

    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed : page {page}")
        result = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    #jobs = extract_jobs(2)
    return jobs
