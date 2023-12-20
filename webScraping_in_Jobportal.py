from bs4 import BeautifulSoup
import requests
import pandas as pd

import pandas as pd
columns_list = ['Job Title','Job URL','Job Location','Line of Business','Job Code','Primary Skills']

df = pd.DataFrame(columns = columns_list)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def get_job_url(url, df):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    jobs = soup.find_all('div', class_='job-list-wrap job_list')

    for job in jobs:
        print(job.a['href'])
        job_title = job.h4.text
        job_url = job.a['href']

        response = requests.get(job_url, headers=headers)
        soup_2 = BeautifulSoup(response.text, 'lxml')

        primary_skills = soup_2.find('div', class_='_detail-content')
        try:
            # print(primary_skills.find('h6').text)
            primary_skills_list = primary_skills.find('li').text
        except:
            primary_skills_list = f'{primary_skills.h1.text} doesn\'t have skills mentioned'

        desc = job.find_all('span')
        job_location = desc[0].text
        line_of_business = desc[1].text
        job_code = desc[2].text

        row_item = [job_title, job_url, job_location, line_of_business, job_code, primary_skills_list]
        print(row_item)
        lenght = len(df)
        df.loc[lenght] = row_item

    return df


for i in range(1,12):
    print(f'page:{i}')
    url = f'https://careers.brillio.com/job-listing/page/{i}/?job_title&country&workplace'
    print(url)
    get_job_url(url,df)
    print('\n')

print(df)
df.to_csv(r'D:\Python\Brillio_jobs.csv',index = False )
