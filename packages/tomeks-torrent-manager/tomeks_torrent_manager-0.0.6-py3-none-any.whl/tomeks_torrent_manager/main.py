#!/bin/python
import sys

from pull_torrent_info.download_from_website import pull_website_history
from pull_torrent_info.download_from_transmission import pull_transmission_data
from pull_torrent_info.download_rss_feeds import pull_rss_feeds


if __name__ == "__main__":
    for function in sys.argv[1:]:
        match function:
            case "web":
                pull_website_history()

            case "trans":
                pull_transmission_data()

            case "rss":
                pull_rss_feeds()

    if len(sys.argv[1:]) == 0:
        pull_website_history()
        pull_transmission_data()
        pull_rss_feeds()

            

    # pull_website_history()
    # pull_transmission_data()
    # pull_rss_feeds()