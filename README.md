# Sinhala Song Lyrics Search Engine
 
This project is to create a search engine that is capable of searching Sinhala song lyrics using Sinhala text. If there were several approaches to search lyrics using "Singlish", it is rare to find a lyrics search engine to search using sinhala text. In my approach I used python 3.6.5 as the programming language and elastic search to create the search engine.

## Technologies that have used

  - Python 3.6.5
  - Elasticsearch 7.8.0
  - Scrapy for web scraping
  - "googletranslate" python library
  - Flask for web api
  - "[Sinling](https://github.com/ysenarath/sinling.git)" project for sinhala tokenizer 

## Content

  - Envirenment Setup
    - Python Envirenment 
    - Elasticsearch
    - Flask
  - Web Scraping
  - Indexing and Mapping
  - Guideline of possible query types
  - Future Works

## Envirenment Setup
### Python Envirenment
This project have used python 3.6.5. You can easily configure the python envirenment according to the platform that youa are using.

Next, install "scrapy", "flask" and "googletrans" libraries for python using python "pip".
- scrapy
``` pip install scrapy ```
- flask
``` pip install flask ```
- Google translate
``` pip install googletrans```

### Elasticsearch

You can find elasticsearch project from official website [here](https://www.elastic.co/downloads/elasticsearch).

Then you can run elastic server,
- Windows
``` ${path to the elasticsearch library}/bin/elasticsearch.bat```
- Linux
-``` ${path to the elasticsearch library}/bin/elasticsearch```

> Note:  Default port number of the elasticsearch server is 9200. You can change it as you wish using elasticsearch configurations.

### Flask
First navigate into the directory ``${project root}/UI``. Then you can start the web UI using flask as
``` python -m flask run ```

Then the running api can be access by `` http:// localhost:5000 ``
> Note:  Default port number of the flask root endpoint is 5000. You can change it as you wish using flask configurations.

## Web Scraping
This project uses scrapy library for python to scrape sinhala song lyrics and meta data. For guidlines [visit](https://docs.scrapy.org/en/latest/).

Output data included in `` ${project root}/data `` directory as a `` json `` file. Data consists including 11 fields,
- name
- artist_en,
- artist_si
- genre_en
- genre_si
- composer_en
- composer_si
- music_en
- music_si
- views
- lyrics

Json structure as follows,

> [
>   {"name":"sss", "artist_en": "sss", "artist_en": "sss", ...},
>   {..},
>   {..},
>   ...
>]

## Indexing and Mapping
Several advance methods are used to create index and map above scrapped data into elasticsearch. Required resources are available [here](https://www.elastic.co/downloads/elasticsearch) .

## Guidline for possible queries
This project can handle several basic queries and some advance queries. For example, this system has the capability to handle basic queries like "අමරදේව,"වක්කඩ ලග , etc. and some advace queries like "අමරදේව ගැයූ ගී","අමරදේව ගැයූ හොදම ගීත", etc.

- Search interface
![Screenshot 1](/images/sc1.jpeg)

- Output
![Screenshot 2](/images/sc2.jpeg)

However, The system can not handle the queries contains combined words like "අමරදේවගේ" yet.

## Future works

Although the system have implemented some advance query methods there are some more to achieve like above mensioned combined word identification, aggregation, etc. These options will be added soon and the system will be improved to process both Sinhala and singlish queries. 
