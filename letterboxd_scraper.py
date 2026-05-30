import urllib.request
import argparse
import pandas as pd
import sys
import time
import os
from bs4 import BeautifulSoup
from fastapi import HTTPException


def fetch_html(url):

    headers = {"User-Agent": "Mozilla/5.0"}
    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        html = response.read().decode("utf-8")
    return html

def find_titles(user: str):# 1. Find ONE element with any data-item-name value
    
    blankPage = False
    iteration = 0
    elements_titles = []


    while not blankPage:
        elements = []
        if iteration == 0:
            url = 'https://letterboxd.com/'+user+'/watchlist/'
        else:
            url = 'https://letterboxd.com/'+user+'/watchlist/page/'+str(iteration+1)+'/'

        html = fetch_html(url)
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.find_all(attrs={"data-item-name": True})

        for element in elements:
            elements_titles.append(element["data-item-name"])
        iteration += 1
        if len(elements) == 0:
            blankPage = True

    return elements_titles

def separate_in_title_year(titlesAndYears: str):

    titles = []
    years = []

    for titleAndYear in titlesAndYears:
        titles.append(titleAndYear.split('(')[0])

        # Some movies may not have a year
        if len(titleAndYear.split('(')) == 1:
            years.append('')
        else:
            years.append(titleAndYear.split('(')[1].split(')')[0])

    return titles, years

def print_title_list(titles: list):
    
    print('\nWatchlist:\n')
    for title in titles:
        print(title)
    print('\n')

def retrive_watchlist_from_user(user: str):
    try:
        titlesAndYears = find_titles(user)
        if len(titlesAndYears) == 0:
            return pd.DataFrame( columns=['Name', 'Year'])
        else:

            titles, years = separate_in_title_year(titlesAndYears)
            d = pd.DataFrame(titles, columns=['Name'])
            d['Year'] = years
            
            return d
    except :
        return HTTPException(status_code=404, detail=f"User {user} not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve watchlist from letterboxd username")
    parser.add_argument('users', help='Username of one or more users', nargs='+')
    date = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    args = parser.parse_args()

    output_dir = f"watchlists"
    os.makedirs(output_dir, exist_ok=True)

    for user in args.users:
        try:
            df = retrive_watchlist_from_user(user)
            print_title_list(df['Name'])

            # On utc
            nameToStore = f"{output_dir}/watchlist-{user}-{date}-utc.csv"

            df.to_csv(nameToStore, index=False)

            print(f'Stored on {nameToStore}')
        except:
            # Nothing but dont fail
            print(f"Username {user} doesn't exist")
            pass
