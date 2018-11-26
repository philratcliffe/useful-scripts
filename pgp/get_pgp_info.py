import pprint
import requests
import sys


# Example: python get_pgp_info.py fred@flintstone.com get

def get_info_from_keyserver(search_term, op_value="index"):

    url = "https://hkps.pool.sks-keyservers.net/pks/lookup"
    payload = {'op':op_value, 'search':search_term, 'options':'mr'}
    response = requests.get(url, params=payload, verify='sks-keyservers.net-CA.pem')
    print(response.url)
    return response.text


if __name__ == '__main__':

    arg_list = []
    arg_count = len(sys.argv)
    print(arg_count)

    if (arg_count < 2) or (arg_count > 3):
        sys.exit("\n\nUsage: {} search_term [op_value]\n\n".format(sys.argv[0]))

    arg_list.append(sys.argv[1])
    if arg_count > 2:
        arg_list.append(sys.argv[2])

    html_result = get_info_from_keyserver(*arg_list)
    pprint.pprint(html_result)
