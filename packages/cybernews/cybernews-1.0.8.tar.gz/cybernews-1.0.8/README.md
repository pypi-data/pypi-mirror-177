<h1>cybernews</h1>
Python package and API that provides latest Cyber Security updates from various sources under one roof and use Web-Scraping under the hood.

<br>
<h2>Public REST API</h2>

```
https://cyber-news-api.herokuapp.com/
```

<h2>Features :-</h2>


```
 News Headlines
 News Author
 Full News
 News Article URL
 News Image
 News Date
```
<br>
Developed by GhoulBond (c) 2021<br><br>

<h2>Setup</h2>


<h3>For Window Users</h3>

```python
pip install cybernews 
```

<h3>For Linux/Mac Users</h3>

```python
pip3 install cybernews
```

<h2>Use</h2>

```python
from cybernews import cybernews
news = cybernews.CyberNews() #Instance is created
```

<h2>All Functionalities</h2>

| **S.No.** | **Operation**      | **Functions**        | **API**                                            |
|-----------|--------------------|----------------------|----------------------------------------------------|
| 1         | Basic News         | news.basic()         | https://cyber-news-api.herokuapp.com/basic         |
| 2         | Data Breach News   | news.dataBreach()    | https://cyber-news-api.herokuapp.com/dataBreach    |
| 3         | Cyber Attack News  | news.cyberAttack()   | https://cyber-news-api.herokuapp.com/cyberAttack   |
| 4         | Vulnerability News | news.vulnerability() | https://cyber-news-api.herokuapp.com/vulnerability |
| 5         | Malware News       | news.malware()       | https://cyber-news-api.herokuapp.com/malware       |
| 6         | Security News      | news.security()      | https://cyber-news-api.herokuapp.com/security      |
| 7         | Cloud News         | news.cloud()         | https://cyber-news-api.herokuapp.com/cloud         |
| 8         | Tech News          | news.tech()          | https://cyber-news-api.herokuapp.com/tech          |
| 9         | IOT News           | news.iot()           | https://cyber-news-api.herokuapp.com/iot           |
| 10        | Big Data News      | news.bigData()       | https://cyber-news-api.herokuapp.com/bigData       |
| 11        | Business News      | news.business()      | https://cyber-news-api.herokuapp.com/business      |
| 12        | Mobility News      | news.mobility()      | https://cyber-news-api.herokuapp.com/mobility      |
| 13        | Research News      | news.research()      | https://cyber-news-api.herokuapp.com/research      |
| 14        | Corporate News     | news.corporate()     | https://cyber-news-api.herokuapp.com/corporate     |
| 15        | Social Media News  | news.socialMedia()   | https://cyber-news-api.herokuapp.com/socialMedia   |
