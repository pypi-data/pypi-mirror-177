from datetime import datetime
from datasize import DataSize

def filesize_string_to_bytes(filesize_string):
    return int(DataSize(filesize_string.strip().replace(' ', '')))

def datestring_standardise(date_string, format):
    return datetime.strptime(date_string, format).strftime("%Y-%m-%d %H:%M:%S")

def datestring_to_int(date_string, format):
    # '%d %b %Y %H:%M'
    # '%b %d, %Y'
    return int(datetime.strptime(date_string, format).timestamp())
    pass
