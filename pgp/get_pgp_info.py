import pprint
import requests
import sys
from urlparse import urlparse

SERVERS = ["hkps://hkps.pool.sks-keyservers.net"]

# Example: python get_pgp_info.py fred@flintstone.com get

def get_info_from_keyserver(search_term, op_value="index"):

    for key_server in SERVERS:
        parse_result = urlparse(key_server)
        url = "https://{}/{}".format(parse_result.netloc, 'pks/lookup')
        payload = {'op':op_value, 'search':search_term, 'options':'mr',\
                'fingerprint':'on'}

        # Note: the CA verification cert is now included in this file.
        response = requests.get(url, params=payload, verify=__file__)

        if (search_term in response.text):
            break
    return response.text


if __name__ == '__main__':

    arg_list = []
    arg_count = len(sys.argv)

    if (arg_count < 2) or (arg_count > 3):
        sys.exit("\n\nUsage: {} search_term [op_value]\n\n".format(sys.argv[0]))

    arg_list.append(sys.argv[1])
    if arg_count > 2:
        arg_list.append(sys.argv[2])

    html_result = get_info_from_keyserver(*arg_list)
    pprint.pprint(html_result)


SKS_SERVERS_CA_CERT = """
-----BEGIN CERTIFICATE-----
MIIFizCCA3OgAwIBAgIJAK9zyLTPn4CPMA0GCSqGSIb3DQEBBQUAMFwxCzAJBgNV
BAYTAk5PMQ0wCwYDVQQIDARPc2xvMR4wHAYDVQQKDBVza3Mta2V5c2VydmVycy5u
ZXQgQ0ExHjAcBgNVBAMMFXNrcy1rZXlzZXJ2ZXJzLm5ldCBDQTAeFw0xMjEwMDkw
MDMzMzdaFw0yMjEwMDcwMDMzMzdaMFwxCzAJBgNVBAYTAk5PMQ0wCwYDVQQIDARP
c2xvMR4wHAYDVQQKDBVza3Mta2V5c2VydmVycy5uZXQgQ0ExHjAcBgNVBAMMFXNr
cy1rZXlzZXJ2ZXJzLm5ldCBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoC
ggIBANdsWy4PXWNUCkS3L//nrd0GqN3dVwoBGZ6w94Tw2jPDPifegwxQozFXkG6I
6A4TK1CJLXPvfz0UP0aBYyPmTNadDinaB9T4jIwd4rnxl+59GiEmqkN3IfPsv5Jj
MkKUmJnvOT0DEVlEaO1UZIwx5WpfprB3mR81/qm4XkAgmYrmgnLXd/pJDAMk7y1F
45b5zWofiD5l677lplcIPRbFhpJ6kDTODXh/XEdtF71EAeaOdEGOvyGDmCO0GWqS
FDkMMPTlieLA/0rgFTcz4xwUYj/cD5e0ZBuSkYsYFAU3hd1cGfBue0cPZaQH2HYx
Qk4zXD8S3F4690fRhr+tki5gyG6JDR67aKp3BIGLqm7f45WkX1hYp+YXywmEziM4
aSbGYhx8hoFGfq9UcfPEvp2aoc8u5sdqjDslhyUzM1v3m3ZGbhwEOnVjljY6JJLx
MxagxnZZSAY424ZZ3t71E/Mn27dm2w+xFRuoy8JEjv1d+BT3eChM5KaNwrj0IO/y
u8kFIgWYA1vZ/15qMT+tyJTfyrNVV/7Df7TNeWyNqjJ5rBmt0M6NpHG7CrUSkBy9
p8JhimgjP5r0FlEkgg+lyD+V79H98gQfVgP3pbJICz0SpBQf2F/2tyS4rLm+49rP
fcOajiXEuyhpcmzgusAj/1FjrtlynH1r9mnNaX4e+rLWzvU5AgMBAAGjUDBOMB0G
A1UdDgQWBBTkwyoJFGfYTVISTpM8E+igjdq28zAfBgNVHSMEGDAWgBTkwyoJFGfY
TVISTpM8E+igjdq28zAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4ICAQAR
OXnYwu3g1ZjHyley3fZI5aLPsaE17cOImVTehC8DcIphm2HOMR/hYTTL+V0G4P+u
gH+6xeRLKSHMHZTtSBIa6GDL03434y9CBuwGvAFCMU2GV8w92/Z7apkAhdLToZA/
X/iWP2jeaVJhxgEcH8uPrnSlqoPBcKC9PrgUzQYfSZJkLmB+3jEa3HKruy1abJP5
gAdQvwvcPpvYRnIzUc9fZODsVmlHVFBCl2dlu/iHh2h4GmL4Da2rRkUMlbVTdioB
UYIvMycdOkpH5wJftzw7cpjsudGas0PARDXCFfGyKhwBRFY7Xp7lbjtU5Rz0Gc04
lPrhDf0pFE98Aw4jJRpFeWMjpXUEaG1cq7D641RpgcMfPFvOHY47rvDTS7XJOaUT
BwRjmDt896s6vMDcaG/uXJbQjuzmmx3W2Idyh3s5SI0GTHb0IwMKYb4eBUIpQOnB
cE77VnCYqKvN1NVYAqhWjXbY7XasZvszCRcOG+W3FqNaHOK/n/0ueb0uijdLan+U
f4p1bjbAox8eAOQS/8a3bzkJzdyBNUKGx1BIK2IBL9bn/HravSDOiNRSnZ/R3l9G
ZauX0tu7IIDlRCILXSyeazu0aj/vdT3YFQXPcvt5Fkf5wiNTo53f72/jYEJd6qph
WrpoKqrwGwTpRUCMhYIUt65hsTxCiJJ5nKe39h46sg==
-----END CERTIFICATE-----
"""

