import feedparser
import re
from datetime import datetime
from .utils import filesize_string_to_bytes, datestring_to_int, datestring_standardise
from .database import con
from tqdm import tqdm
import os

feed_urls = [
    {
        'name': 'avistaz',
        'filters': ['Free Download', 'Double Upload'],
        'url':  os.environ['AVISTAZ_RSS'],
    },
    {
        'name': 'cinemaz',
        'filters': ['Free Download', 'Double Upload'],
        'url':  os.environ['CINEMAZ_RSS'],
    },
]
cur = con.cursor()

def find_regex_entry(regex_code, entry, data_type):
    try:
        match = re.findall(regex_code, entry)[0]
        if data_type == 'filesize_int':
            return filesize_string_to_bytes(match)
        elif  data_type == 'date':
            return datestring_standardise(match, '%b %d, %Y')
        else:
            return match
    except IndexError:
        if data_type in ('filesize_int',  'date_int'):
            return 0
        else:
            return data_type

def pull_rss_feeds():
    today = datetime.now()
    today_string = today.strftime("%Y-%m-%d_%H:%M:%S")

    cur.execute('DELETE FROM stg_torrent_rss;')

    for feed_url in feed_urls:
        url_to_download = feed_url['url']
        site_name = feed_url['name']

        feed = feedparser.parse(url_to_download)

        regex = [
            ('type', '<strong>Type<\/strong>: (.+?)<br \/>', ''),
            ('size', '<strong>Size<\/strong>: (.+?)<br \/>', 'filesize_int'),
            ('uploaded', '<strong>Uploaded<\/strong>: (.+?)<br \/>', 'date'),
            ('seed', 'Seed<\/strong>: (\d+) \| ', 0),
            ('leech', 'Leech<\/strong>: (\d+) \| ', 0),
            ('completed', 'Completed<\/strong>: (\d+)', 0.0),
            ('site_url', 'href="(.+?)" title=', ''),
        ]

        # re.findall('<strong>File Name<\/strong>: (.+?)<br \/>', feed.entries[1].summary)[0]

        nice_results = []
        db_results = []


        for entry in tqdm(feed.entries):
            result = { regex_name: find_regex_entry(regex_code, entry.summary, data_type) for (regex_name, regex_code, data_type) in regex }

            result['title'] = entry.title
            result['torrent_url'] = entry.link
            result['author'] = entry.author
            result['published'] = datestring_standardise(entry.published, '%a, %d %b %Y %H:%M:%S %z')
            result['infohash'] = entry.infohash

            rss_bk = f"{result['infohash']}/{today_string}"
            result['bk'] = rss_bk      

            data = [
                (
                    result['torrent_url'],                
                    result['infohash'],
                    site_name,
                    '/'.join(feed_url['filters']),
                    result['type'],
                    result['size'],
                    result['uploaded'],
                    result['seed'],
                    result['leech'],
                    result['completed'],
                    result['site_url'],
                    result['title'],
                    result['author'],
                    result['published'],
                ),
            ]
            
            db_results.append(data)
            nice_results.append(result)


            cur.executemany("""
                INSERT INTO stg_torrent_rss(
                    torrent_url,
                    infohash,
                    site,
                    rss_filter,
                    media_type,
                    torrent_size,
                    date_uploaded,
                    seed_users,
                    leech_users,
                    completed,
                    site_url,
                    title,
                    author,
                    published
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)
    
    con.commit()
