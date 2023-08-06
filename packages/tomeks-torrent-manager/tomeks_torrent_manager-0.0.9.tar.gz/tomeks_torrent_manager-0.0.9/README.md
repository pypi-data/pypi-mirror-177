# Tomeks torrent manager

:D

Source: https://packaging.python.org/en/latest/tutorials/packaging-projects/


## Build
```
python3 -m build
```

# Testing
## Install from local
```
python -m venv venv
pip uninstall tomeks-torrent-manager
pip install dist/tomeks_torrent_manager-*.tar.gz
```

## Upload to test
```
python3 -m twine upload --repository testpypi dist/*
```

## Install from test Pypi
```
python3 -m pip install --index-url https://test.pypi.org/simple/ tomeks_torrent_manager
```

# Prod
# Upload to prod
```
python3 -m twine upload dist/*
```





# How to use
```
from tomeks_torrent_manager.pull_torrent_info import download_from_transmission, download_from_website, download_rss_feeds
download_from_website.pull_website_history()

```