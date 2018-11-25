import pprint
import requests
import sys


def get_pgp_key(search_term):

    url = "https://hkps.pool.sks-keyservers.net/pks/lookup?op=index&search={}".format(search_term)
    print(url)
    response = requests.get(url, verify='sks-keyservers.net-CA.pem')
    return response.text


if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit("\n\nUsage: {} search_term\n\n".format(sys.argv[0]))
    search_term = sys.argv[1]
    html_result = get_pgp_key(search_term)
    pprint.pprint(html_result)



