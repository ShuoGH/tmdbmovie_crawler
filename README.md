## Web Crawler for the Movie Poster in tmdb
### File Catalog: 

- **images**
    - File folder to store the posters
    - The name of images is given by: `[movieId]-[movie name]-[tmdbId].jpg`
- get_proxies.py 
    - Scrape the proxies from Internet
    - Check whether these proxies are useful for our work.
- Links_small.csv
    - movie list
- Movie_crawler_demo.ipynb
    - jupyter notebook which is used in the beginning of coding for testing
- Movie_crawler.py
    - the crawler for crawling posters

### Environments

- python3
- Fake_useragent
- bs4 
- Pandas, numpy
- requests 

### How to run

- activate python3 environment
- run `python get_proxies.py` to get the proxies file
- build `images` file folder by typing `mkdir images` in the terminal
- put the `links_small.csv` file into the current file folder
- run python `movie_crawler.py` in the terminal 
- waiting for completion (may need a long time since I set a time of sleeping during each poster)