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
from tomeks_torrent_manager import torrent_manager
torrent_manager.pull_transmission()
torrent_manager.pull_website_history()
torrent_manager.pull_rss()

```