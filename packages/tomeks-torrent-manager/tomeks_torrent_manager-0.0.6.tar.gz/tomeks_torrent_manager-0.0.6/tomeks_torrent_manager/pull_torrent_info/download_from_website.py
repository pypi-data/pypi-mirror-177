import requests
import json
from bs4 import BeautifulSoup as bs
# import pandas as pd
import re
from time import sleep
from pytimeparse.timeparse import timeparse
from datetime import datetime, date, time, timedelta
from datasize import DataSize
import sqlite3
import os.path
from tqdm import tqdm

from .database import con
from .utils import filesize_string_to_bytes

# Store network urls, as well as common headers
networks = {
    'avistaz': {
        'sites': [
            {
                'name':     'avistaz',
                'url':      'https://avistaz.to',
                'cookie':    os.environ['AVISTAZ_COOKIE']
            },
            {
                'name':     'cinemaz',
                'url':      'https://cinemaz.to',
                'cookie':    os.environ['CINEMAZ_COOKIE']
            
            },
        ],
        'headers': {
            'authority': 'avistaz.to',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-AU,en;q=0.9,pl-PL;q=0.8,pl;q=0.7,en-US;q=0.6,en-GB;q=0.5',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Linux',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        }

    }
}


cur = con.cursor()

def generate_headers(network_headers, cookie, url):
    site_specific_headers = {
        'cookie': cookie,
        'referer': url
    }
    return {**network_headers,**site_specific_headers}



# History table functions
def download_history_page(site_url, network_headers, cookie):
    # Pull the torrent history, and insert cookies/url
    payload={}
    history_url = f"{site_url}/profile/superraiden/history" 
    headers = generate_headers(network_headers, cookie, history_url)

    res = requests.request("GET", history_url, headers=headers, data=payload)
    return res.text

def parse_history_table(history_page_text):
    # Parse the text we downloaded
    soup = bs(history_page_text, 'html.parser')

    # Create headers to be able to convert a row into a dictionary
    try:
        history_table = soup.find('table').find('tbody')
    except Exception:
        print(history_page_text)
        raise ValueError("FAILURE ON history_table = soup.find('table').find('tbody')")
    header_names = [
        'Type', 'File', 'Download Link', 'Active', 'Completed', 'Up',
        'Down', 'Ratio', 'Added', 'Updated', 'Seed Duration', 'Hit and Run'
    ]

    # Create history dict
    torrent_history = []
    for row in soup.find('table').find('tbody').find_all('tr'):
        cells = row.find_all('td')
        torrent_row_info = {header_name: cells[i] for i, header_name in enumerate(header_names)}
        # torrent_history.append( torrent_row_info )
        torrent_url = torrent_row_info['File'].find('a')['href']

        result = {
            'torrent_id':           re.search(r"(\d+).+", torrent_url).groups()[0],
            'torrent_url':          torrent_url,
            'title':                torrent_row_info['File'].find('a')['title'],
            'file_size':            filesize_string_to_bytes(torrent_row_info['File'].find('span', {'title': 'File Size'}).text),

            'uploaded':             filesize_soup_to_bytes(torrent_row_info['Up'].find('span', {'class': 'text-green'})),
            'uploaded_credited':    filesize_soup_to_bytes(torrent_row_info['Up'].find('span', {'class': 'text-blue'})),

            'downloaded':           filesize_soup_to_bytes(torrent_row_info['Down'].find('span', {'class': 'text-red'})),
            'downloaded_credited':  filesize_soup_to_bytes(torrent_row_info['Down'].find('span', {'class': 'text-orange'})),

            'seeders':              int(torrent_row_info['File'].find('span', {'title': 'Seeders'}).text.strip()),
            'leechers':             int(torrent_row_info['File'].find('span', {'title': 'Leechers'}).text.strip()),
            'completed':            int(torrent_row_info['File'].find('span', {'title': 'Completed'}).text.strip()),
        }
        torrent_history.append(result)

    return torrent_history


# Torrent page stuff
def download_torrent_page(torrent_url, network_headers, cookie):
    # Pull the torrent history, and insert cookies/url
    payload={}
    headers = generate_headers(network_headers, cookie, torrent_url)

    res = requests.request("GET", torrent_url, headers=headers, data=payload)
    return res.text

def parse_torrent_page(torrent_page_text):
    soup = bs(torrent_page_text, 'html.parser')
    torrent_info_table = soup.find('table')

    torrent_info = {}
    rowz = torrent_info_table.find('tbody').find_all('tr', recursive=False)
    for i, rowz_raw in enumerate(rowz):
        cells = rowz_raw.find_all('td', recursive=False)
        torrent_info[cells[0].text] = cells[1]

    # Discounts
    discounts = []
    dying_torrent_seconds_left = 0
    dying_torrent_expiry = ''
    # Is row 1 showing any discounts
    if 'Discount' in torrent_info.keys():
        # These are our discounts
        discounts = [discount['title'] for discount in torrent_info['Discount'].find_all('i')]
        # Is it a dying torrent with an expiry?
        if len(torrent_info['Discount'].findAll('div', {'class': 'badge-extra'})) > 1:
            dying_torrent_seconds_left = timeparse(torrent_info['Discount'].find_all('td')[1].find('strong').text)
            dying_torrent_expiry = (datetime.now() + timedelta(seconds=468000)).strftime("%Y-%m-%d %H:%M:%S")


    web_result = {
        'info_hash':                    torrent_info['Info Hash'].text,
        'languages':                    [lang.text.strip() for lang in torrent_info['Audio'].findAll('span')],
        'discounts':                    discounts,
        'dying_torrent_seconds_left':   dying_torrent_seconds_left,
        'dying_torrent_expiry':         dying_torrent_expiry,
        'type':                         torrent_info['Type'].text.strip(),
        'uploaded_at':                  datetime.strptime(torrent_info['Uploaded at'].text.strip().split('\n')[0], '%d %b %Y %H:%M').strftime("%Y-%m-%d %H:%M:%S")


    }
    test = 1
    return web_result


# Utils
def filesize_soup_to_bytes(soup):
    if soup is None:
        return 0
    return filesize_string_to_bytes(soup.text)


# Main function

def pull_website_history():
    # 'Now' variable for load times
    today = datetime.now()
    today_string = today.strftime("%Y-%m-%d_%H:%M:%S")

    cur.execute('DELETE FROM stg_torrent_website;')
    
    # Pull current data for each network/site
    for network_name, network in networks.items():
        for site in network['sites']:
            print(f"Downloading site {site['name']}")
            
            # Download the site's history page
            torrent_history = parse_history_table(
                download_history_page(
                    site['url'],
                    network['headers'],
                    site['cookie']
                )
            )


            # Download info for each torrent
            for torrent_history_row in tqdm(torrent_history):
                #Rate limit
                sleep(1)

                torrent_page_data = parse_torrent_page(
                    download_torrent_page(
                        torrent_history_row['torrent_url'],
                        network['headers'],
                        site['cookie']
                    )
                )

                # Merge data between the history table and the torrent's page
                # Add site and network data
                torrent_data = { **torrent_history_row, **torrent_page_data }
                # torrent_bk = f"{site['name']}/{torrent_data['torrent_id']}/{today_string}"
                
                torrent_data['network_name'] = network_name

                data = [
                    (
                        site['name'],
                        torrent_data['torrent_id'],
                        network_name,
                        torrent_data['torrent_url'],
                        torrent_data['title'],
                        torrent_data['file_size'],
                        torrent_data['uploaded'],
                        torrent_data['uploaded_credited'],
                        torrent_data['downloaded'],
                        torrent_data['downloaded_credited'],
                        torrent_data['seeders'],
                        torrent_data['leechers'],
                        torrent_data['completed']
                    ),
                ]
                cur.executemany("""
                    INSERT INTO stg_torrent_website(
                        site,
                        torrent_id,
                        network_name,
                        torrent_url,
                        title,
                        file_size,
                        uploaded,
                        uploaded_credited,
                        downloaded,
                        downloaded_credited,
                        seeders,
                        leechers,
                        completed
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
        
        con.commit()

if __name__ == "__main__":
    pull_live_history()

