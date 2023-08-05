from bs4 import BeautifulSoup
import requests
import re
import uuid

"""Global Session For Performance"""
session = requests.session()

"""Performance Class for better and fast extracting of data"""


class __Performance:

    def __init__(self):
        """Headers For Performance"""
        self._headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
            'Content-Type': 'application/json; charset=utf-8',
            'server': 'nginx/1.0.4',
            'x-runtime': '148ms',
            'etag': '"e1ca502697e5c9317743dc078f67693f"',
            'Access-Control-Allow-Credentials': 'true',
            'Content-Encoding': 'gzip'
        }

        """Regex Patterns Compilation for Performance"""
        self._pattern1 = re.compile(r'\ue804')
        self._pattern2 = re.compile(r'\ue802')
        self._pattern3 = re.compile(r'\ue804.+')
        self._pattern4 = re.compile(
            r"([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?")


"""Class for Sorting News According to the date"""


class __SortingNews:

    """Months Dictionary"""

    def __init__(self) -> None:
        self._months = {
            'january': '01',
            'february': '02',
            'march': '03',
            'april': '04',
            'may': '05',
            'june': '06',
            'july': '07',
            'august': '08',
            'september': '09',
            'october': '10',
            'november': '11',
            'december': '12'
        }

    """Ordering Date"""

    def _orderingDate(self, individualNews):
        if (individualNews == 'N/A'):
            return 1
        individualNews = individualNews.lower().replace(',', '')
        individualNews = individualNews.split(' ')

        try:
            if (individualNews[0].isnumeric()):
                return int(individualNews[2] + self._months[individualNews[1]] + individualNews[0])

            return int(individualNews[2] + self._months[individualNews[0]] + individualNews[1])

        except:
            return 1

    """Ordering News By Latest Date"""

    def _orderingNews(self, news):

        data = sorted(
            news, key=lambda individualNews: individualNews['id'], reverse=True)

        data = self._orderingID(data)
        return data

    """Giving UUID as _id for each news so that id is distinct"""

    def _orderingID(self, news):

        for individualNews in news:
            individualNews['id'] = uuid.uuid4().int

        return news


"""Class for Exception Handling and Extracting data out of complex strings"""


class __Extracting(__Performance, __SortingNews):

    """Extracting Author Name"""

    def _authorNameExtractor(self, name):
        return self._pattern1.sub('', name)

    """Checking is news or some random advertisement"""

    def _checkAd(self, newsDate):
        if (self._pattern4.search(newsDate) != None):
            return True
        return False

    """Extracting NewsDate"""

    def _newsDateExtractor(self, date, news_date):
        return self._pattern3.sub('', self._pattern2.sub('', date)) if news_date != '' else 'N/A'

    """Extracting Data Using Tags"""

    def _dataExtractor(self, newsHeaders):
        """News Data List"""
        news_data = []

        for news in newsHeaders:
            for key in news:
                url = key
                response = session.get(url, timeout=10, headers=self._headers)
                soup = BeautifulSoup(response.text, 'lxml')
                news_headlines = soup.select(news[key]['headlines'])
                news_author = soup.select(news[key]['author'])
                news_fullNews = soup.select(news[key]['fullNews'])
                news_URL = soup.select(news[key]['newsURL'])
                news_img_URL = soup.select(news[key]['newsImg'])
                news_date = soup.select(
                    news[key]['date']) if news[key]['date'] != None else ''

                for index in range(len(news_headlines)):

                    """Extracting newsDate"""
                    newsDate = self._newsDateExtractor(
                        news_date[index].text.strip(), news_date) if news_date != '' else 'N/A'

                    """Checking Advertisement"""
                    if (self._checkAd(newsDate)):
                        continue

                    complete_news = {

                        'id': self._orderingDate(newsDate),
                        'headlines': news_headlines[index].text.strip(),
                        'author': self._authorNameExtractor(news_author[index].text.strip()),
                        'fullNews': news_fullNews[index].text.strip(),
                        'newsURL': news_URL[index]['href'],
                        'newsImgURL': news_img_URL[index]['data-src'],
                        'newsDate': newsDate
                    }

                    news_data.append(complete_news)

        return self._orderingNews(news_data)


"""Main Class for Extracting/Scraping Data"""


class CyberNews(__Extracting):

    """Basic News"""

    def basic(self):
        """Basic Related Website and Tags"""

        basic_attack_news_type = [
            {'https://cio.economictimes.indiatimes.com/news/internet': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                        'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(basic_attack_news_type)

    """Data Breach News"""

    def dataBreach(self):
        """Data Breach Related Website and Tags"""
        data_breach_news_type = [
            {'https://thehackernews.com/search/label/data%20breach': {'headlines': 'h2.home-title', 'author': '.item-label span',
                                                                      'fullNews': '.home-desc', 'newsImg': '.img-ratio img', 'newsURL': 'a.story-link', 'date': '.item-label'}}
        ]

        return self._dataExtractor(data_breach_news_type)

    """Cyber Attack News"""

    def cyberAttack(self):
        """Cyber Attack Related Website and Tags"""
        cyber_attack_news_type = [
            {'https://thehackernews.com/search/label/Cyber%20Attack': {'headlines': 'h2.home-title', 'author': '.item-label span',
                                                                       'fullNews': '.home-desc', 'newsImg': '.img-ratio img', 'newsURL': 'a.story-link', 'date': '.item-label'}}
        ]

        return self._dataExtractor(cyber_attack_news_type)

    """Vulnerability News"""

    def vulnerability(self):
        """Vulnerabilities Related Website and Tags"""
        vulnerability_news_type = [
            {'https://thehackernews.com/search/label/Vulnerability': {'headlines': 'h2.home-title', 'author': '.item-label span',
                                                                      'fullNews': '.home-desc', 'newsImg': '.img-ratio img', 'newsURL': 'a.story-link', 'date': '.item-label'}}
        ]

        return self._dataExtractor(vulnerability_news_type)

    """Malware News"""

    def malware(self):
        """Malware Related Website and Tags"""
        malware_news_type = [
            {'https://thehackernews.com/search/label/Malware': {'headlines': 'h2.home-title', 'author': '.item-label span',
                                                                'fullNews': '.home-desc', 'newsImg': '.img-ratio img', 'newsURL': 'a.story-link', 'date': '.item-label'}}
        ]

        return self._dataExtractor(malware_news_type)

    """Security News"""

    def security(self):
        """Security Related Website and Tags"""
        security_news_type = [
            {'https://telecom.economictimes.indiatimes.com/tag/hacking': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                          'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}},
            {'https://cio.economictimes.indiatimes.com/news/digital-security': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                                'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(security_news_type)

    """Cloud News"""

    def cloud(self):
        """Cloud Related Website and Tags"""
        cloud_news_type = [
            {'https://cio.economictimes.indiatimes.com/news/cloud-computing': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                               'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(cloud_news_type)

    """Technology News"""

    def tech(self):
        """Technology Related Website and Tags """
        tech_news_type = [
            {'https://telecom.economictimes.indiatimes.com/tag/digitalindia': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                               'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}},
            {'https://cio.economictimes.indiatimes.com/tag/next+gen+tech': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                            'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(tech_news_type)

    """IOT News"""

    def iot(self):
        """IOT Related Website and Tags"""
        iot_news_type = [
            {'https://cio.economictimes.indiatimes.com/news/internet-of-things': {'headlines': '.descBx h3 a',
                                                                                  'author': '.metaTx', 'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(iot_news_type)

    """Big Data News"""

    def bigData(self):
        """Big Data Related Website and Tags"""
        bigData_news_type = [
            {'https://cio.economictimes.indiatimes.com/news/big-data': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                        'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}},
            {'https://cio.economictimes.indiatimes.com/news/data-center': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                           'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(bigData_news_type)

    """Business Analytics News"""

    def business(self):
        """Business Analytics Related Website and Tags"""
        business_news_type = [
            {'https://cio.economictimes.indiatimes.com/news/business-analytics': {'headlines': '.descBx h3 a',
                                                                                  'author': '.metaTx', 'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(business_news_type)

    """Mobility News"""

    def mobility(self):
        """Mobility Related Website and Tags"""
        mobility_news_type = [
            {'https://cio.economictimes.indiatimes.com/news/mobility': {'headlines': '.descBx h3 a', 'author': '.metaTx',
                                                                        'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
        ]

        return self._dataExtractor(mobility_news_type)

    """Research News"""

    def research(self):
        """Research Related Website and Tags"""
        research_news_type = [{'https://cio.economictimes.indiatimes.com/tag/research':
                               {'headlines': '.descBx h3 a', 'author': '.metaTx', 'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
                              ]

        return self._dataExtractor(research_news_type)

    """Corporate News"""

    def corporate(self):
        """Corporate Related Website and Tags"""
        corporate_news_type = [{'https://cio.economictimes.indiatimes.com/news/corporate-news':
                                {'headlines': '.descBx h3 a', 'author': '.metaTx', 'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
                               ]

        return self._dataExtractor(corporate_news_type)

    """Social Media News"""

    def socialMedia(self):
        """Social Media Related Website and Tags"""
        social_news_type = [{'https://cio.economictimes.indiatimes.com/news/social-media':
                             {'headlines': '.descBx h3 a', 'author': '.metaTx', 'fullNews': '.descBx p', 'newsImg': 'figure.avtar a img', 'newsURL': '.descBx a', 'date': None}}
                            ]

        return self._dataExtractor(social_news_type)
