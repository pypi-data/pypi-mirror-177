from clutch import Client
from pathlib import Path
from datetime import datetime
import json
import pathlib
import os

from .utils import datestring_standardise, today_standardised
# from .database import get_con

def safe_serialize(obj):
  default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
  return json.dumps(obj, default=default, indent = 4)

def pull_transmission_data():
    print('Pulling data from transmission')

    directory = os.path.join(os.environ['DATA_DIR'], 'staging/transmission/')
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    (today, today_string) = today_standardised()

    client = Client(
        address=os.environ['TRANSMISSION_URL'],
        username=os.environ['TRANSMISSION_USERNAME'],
        password=os.environ['TRANSMISSION_PASSWORD']
    )
    
    # cur = con.cursor()

    response = client.torrent.accessor(all_fields=True)
    torrents = response.arguments.torrents

    # cur.execute('DELETE FROM stg_torrent_transmission;')
    results = []
    for torrent in torrents:
        torrent_bk = f"{torrent.hash_string}/{today_string}"

        raw_data =  torrent.__dict__
        # extra_data = {
        #     'torrent_bk' : torrent_bk,
        #     'snapshot_datetime': today,
        # }
        data = raw_data

        filtered_fields_data = {key: data[key] for key in data.keys()
            & {
                'hash_string', 'activity_date', 'added_date', 'start_date', 'comment', 'date_created', 'downloaded_ever', 'uploaded_ever',
                'magnet_link', 'name', 'seconds_downloading', 'seconds_seeding', 'total_size', 'upload_ratio', 'seconds_seeding',
                'queue_position', 'rate_download', 'rate_upload', 'percent_done', 'peers_connected', 'peers_getting_from_us', 'peers_sending_to_us',
                'is_stalled', 'eta', 'error', 'error_string', 'done_date'
            }}
        filtered_fields_data['snapshot_datetime'] = today_string

        for field in ['done_date', 'date_created', 'start_date', 'activity_date']:
            filtered_fields_data[field] =  datestring_standardise(datetime.fromtimestamp(filtered_fields_data[field]))


 

        results.append(filtered_fields_data)

    filename = f'{today_string}.json'
    full_filepath = os.path.join(directory, filename)

    with open(full_filepath, 'w') as fp:
        json.dump(results, fp)
    
