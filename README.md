# Scrapy
All my Scrapy projects are here

## Garagem

This project aims to scrap data from books printed by the major brands and solded in Saraiva website.

### Configuration
First of all, you need a Splash instance running. You are able to do that by running a Docker image:

`$ docker run -p 8050:8050 scrapinghub/splash`

You must also add the Splash server address to `./garagem/garagem/settings.py` like this:

`SPLASH_URL = 'http://192.168.59.103:8050'`

### Executing SaraivaSpider
Currently, there is no script to execute the Spider autonomously. It requires doing it from Terminal.

To start crawling, you must be located at `garagem` folder (the outermost one) and send this command:

`$ scrapy crawl saraiva`

if you want to dump the items in a JSON Lines file like I did with `saraiva.jl`, just add `-o FILENAME.jl` to the command above.

You may access [Scrapy Docs](https://docs.scrapy.org/en/latest/index.html) for further options and Documentation.
