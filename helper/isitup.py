'''
isitup.org helper module
(c) 2018 - laymonage
'''

from urllib.parse import urlparse
import requests


def isup(site, detailed=False):
    '''
    Return site up or down status received from https://isitup.org.
    site (str): site to be checked
    detailed (bool): if true, add IP, response code, and response time info
    '''
    if not site.startswith('http'):
        url = 'http://{}'.format(site)
    else:
        url = site
    domain = urlparse(url).netloc
    api_url = 'https://isitup.org/{}.txt'.format(domain)

    try:
        data = requests.get(api_url).text
        data = data.split(', ')
        status_code = int(data[2])
    except requests.exceptions.ConnectionError:
        status_code = 4

    if status_code == 1:
        result = "{} is up.".format(site)
    elif status_code == 2:
        result = "{} seems to be down.".format(site)
    elif status_code == 3:
        result = "{} is not a valid domain.".format(site)
    elif status_code == 4:
        result = "Sorry, the isitup.org service seems to be down."
    else:
        result = "Sorry, I encountered an error in the API."

    if detailed and status_code == 1:
        result += ("\nIP: {}"
                   "\nResponse code: {}"
                   "\nResponse time: {} ms"
                   .format(data[3], data[4], float(data[5])*1000))

    return result
