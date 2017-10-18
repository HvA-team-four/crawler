import urllib.request
import urllib.error
import urllib
import logging
import socket


def setup_logfile(name):
    # Setting up logging
    logging.basicConfig(filename=str(name) + '.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
    logging.info('\n----------------------------------------------------------------------------------------'
                 '\n Logging started')


def content_crawler(url):
    # crawls the content
    setup_logfile("content")

    webcontent = None

    print("Crawling URL:" + url)
    logging.info('Trying to open ' + url)

    # request to onion site, open url and read contents
    try:
        webcontent = urllib.request.urlopen(url, timeout=10).read()
    except (urllib.error.HTTPError, urllib.error.URLError) as error:
        print("Error retrieving website: ", url)
        logging.error('Data not retrieved from URL: ' + url + ' because error ' + str(error))
    except socket.timeout:
        print("timeout")
        logging.error('Socket timed out, unable to retrieve data from URL: ' + url)
    return webcontent
