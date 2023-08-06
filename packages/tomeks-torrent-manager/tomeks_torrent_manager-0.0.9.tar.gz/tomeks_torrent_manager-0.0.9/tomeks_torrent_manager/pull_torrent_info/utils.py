from datetime import datetime
from datasize import DataSize

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

def today_standardised():
    today = datetime.utcnow()
    today_string = today.strftime(ISO_FORMAT)

    return(today, today_string)

def filesize_string_to_bytes(filesize_string):
    return int(DataSize(filesize_string.strip().replace(' ', '')))

def datestring_standardise(date, format=None):
    if format:
        return datetime.strptime(date, format).strftime(ISO_FORMAT)
    else:
        return date.strftime(ISO_FORMAT)

def datestring_to_int(date_string, format):
    # '%d %b %Y %H:%M'
    # '%b %d, %Y'
    return int(datetime.strptime(date_string, format).timestamp())
