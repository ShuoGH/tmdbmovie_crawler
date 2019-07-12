import requests
from bs4 import BeautifulSoup
from time import sleep
import os
import random
from fake_useragent import UserAgent
import json
import pandas as pd
import numpy as np

PROJECT_PATH = os.getcwd()
IMAGE_PATH = os.getcwd() + '/images/'
ip_random = -1


def header(fake_ua, referer):
    '''
    Using the fake_useragent to randomly choose your useragent to avoid the anti-spider tech.
    It seems that you don't need to update the referer always in this case
    '''
    headers = {
        'User-Agent': fake_ua,
        'Referer': '{}'.format(referer),
    }
    return headers


def get_proxie(random_number):
    '''
    Read the proxies from the ip_movie.txt file
    '''
    with open(PROJECT_PATH + '/ip_movie.txt', 'r') as file:
        ip_list = json.load(file)
        if random_number == -1:
            random_number = random.randint(0, len(ip_list) - 1)
        ip_info = ip_list[random_number]
        ip_url_next = '://' + ip_info['address'] + ':' + ip_info['port']
        proxies = {'http': 'http' + ip_url_next}
        return random_number, proxies


def random_sleep_time():
    '''
    random generate the time of sleeping when doing the scraping work
    '''
    possibility_like = random.random()
    if possibility_like < 0.2:
        sleep_time = random.randint(10, 20)
    else:
        sleep_time = random.randint(1, 10)
    return sleep_time


def read_movie_list():
    '''
    return the `movie id` and `movie tmdb id` 
    We would use the movie tmdb id to request the web page

    Note: 
        drop nan (clean the data frame)
    '''
    movie_list_all = pd.read_csv("links_small.csv")
    movie_list_all_nonan = movie_list_all.dropna()

    movie_id_tmdbid = np.array([(str(int(row['movieId'])), str(
        int(row['tmdbId']))) for index, row in movie_list_all_nonan.iterrows()])

    return movie_id_tmdbid


def get_images(movie_id, tmdbId, referer):
    # ---- Every time when opening the link, randomly choose one useragent ----
    fake_ua = UserAgent()
    user_agent = fake_ua.random
    # ---- Randomly choose the proxies ----
    global ip_random
    ip_rand, proxies = get_proxie(ip_random)
    movie_url = "https://www.themoviedb.org/movie/{}".format(str(tmdbId))
    try:
        movie_page_r = requests.get(movie_url, headers=header(
            user_agent, referer), proxies=proxies)
        # print("first try for this movie: {}, type{}".format(
        #     movie_page_r, type(movie_page_r)))
        response_status_code = 200
    except:
        print("not successful for this ip {}".format(proxies["http"]))
        n = 1
        response_status_code = 500
    while response_status_code != 200:
        ip_random = -1
        ip_rand, proxies = get_proxie(ip_random)
        print("try another proxies {}".format(proxies["http"]))
        try:
            print("another try for this movie: {}".format(movie_url))
            movie_page = requests.get(movie_url, headers=header(
                user_agent, referer), proxies=proxies)
            response_status_code = 200
        except:
            print("not successful for this ip {}".format(proxies["http"]))
            response_status_code = 500
            n += 1
            if n >= 50:
                raise Exception("Try enough unavailable ip address")
    soup = BeautifulSoup(movie_page_r.text, features="html.parser")

    # get the url of the poster, movie tile
    image_url = soup.find('div', class_='image_content').find('a')['href']
    movie_title = soup.find('div', class_="title").find('h2').text

    os.chdir(IMAGE_PATH)
    # ---- downloading the images ----
    image_referer = movie_url
    # name of the poster on your disk
    pic_name = "{}-{}-{}.jpg".format(movie_id, movie_title, tmdbId)

    sleep(random_sleep_time())
    f = open(pic_name, 'wb')
    print("accessing {} of movie {}..".format(image_url, movie_title))
    f.write(requests.get(image_url, headers=header(
        user_agent, image_referer), proxies=proxies).content)
    f.close()
    print("finish the poster of : {}".format(movie_title))


if __name__ == "__main__":
    '''
    remember to update the referer when you change the page number.
    '''
    header_referer = "https://www.themoviedb.org/movie"
    movie_id_tmdbid_list = read_movie_list()
    for mid, mtid in movie_id_tmdbid_list:
        get_images(mid, mtid, header_referer)
        while int(mid) % 100 == 0:
            print("finish the {}th poster".format(mid))
    print("all done")
