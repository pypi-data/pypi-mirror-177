from clutch import Client
from pathlib import Path
from .database import con
from datetime import datetime
import json
import os

def safe_serialize(obj):
  default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
  return json.dumps(obj, default=default, indent = 4)

def pull_transmission_data():
    print('Pulling data from transmission')

    today = datetime.now()
    today_string = today.strftime("%Y-%m-%d_%H:%M:%S")

    client = Client(
        address=os.environ['TRANSMISSION_URL'],
        username=os.environ['TRANSMISSION_USERNAME'],
        password=os.environ['TRANSMISSION_PASSWORD']
    )
    
    cur = con.cursor()

    response = client.torrent.accessor(all_fields=True)
    torrents = response.arguments.torrents

    cur.execute('DELETE FROM stg_torrent_transmission;')
    
    for torrent in torrents:
        torrent_bk = f"{torrent.hash_string}/{today_string}"

        raw_data =  torrent.__dict__
        extra_data = {
                'torrent_bk' : torrent_bk,
                'snapshot_datetime': today,
        }
        data = raw_data | extra_data
        
        insert_row = [
            (
                data['hash_string'],
                data['activity_date'],
                data['added_date'],
                data['comment'],
                data['date_created'],
                data['downloaded_ever'],
                data['hash_string'],
                data['magnet_link'],
                data['name'],
                data['seconds_downloading'],
                data['seconds_seeding'],
                data['total_size'],
                data['upload_ratio']
            ),
        ]
        cur.executemany(
            """INSERT INTO stg_torrent_transmission(
                    filehash,
                    activity_date,
                    added_date,
                    comment,
                    date_created,
                    downloaded_ever,
                    hash_string,
                    magnet_link,
                    name,
                    seconds_downloading,
                    seconds_seeding,
                    total_size,
                    upload_ratio
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", insert_row)
    
    con.commit()