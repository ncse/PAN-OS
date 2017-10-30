import click
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xml.etree.ElementTree as ET
import sys

# url_list should be formatted as single line entries in a flat text file
# output file will default to directory you are running the script in, unless otherwise changed
# TODO: Put some error checking and correcting in

@click.command()
@click.option('--device', prompt=True, help='Firewall management IP')
@click.option('--user', prompt=True, help='User account that has access to the API')
@click.option('--pw', prompt=True, hide_input=True, help='User account password')
@click.option('--url_list', prompt=True, help='Location of your flat text file')
@click.option('--output_file', prompt=True, help='Output file location, specify .csv for best results' )


def check_urls(device, user, pw, url_list, output_file):

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    sys.stdout = open(output_file, 'w')

    key_url = 'https://%s/api/?type=keygen&user=%s&password=%s' % (device, user, pw)
    key_req = requests.get(key_url, verify=False)
    response = key_req.content
    root = ET.fromstring(response)

    for key_val in root.findall('.//key'):
        api_key = key_val.text

    with open (url_list, "r") as url_file:
        for line in url_file:
            url_to_test = line
            url_test_url = 'https://%s/api/?type=op&cmd=<test><url>%s</url></test>&key=%s' % (device, url_to_test, api_key)
            test_req = requests.get(url_test_url, verify=False)
            test_response = test_req.content
            test_root = ET.fromstring(test_response)

            for resp_val in test_root.findall('.//result'):
                url_category = resp_val.text
                url_response = url_category.split("\n")
                url = url_response[0]
                url_base_class = url_response[1]
                url_base_class_formatted = url_base_class.split(" ")
                url_base_class_response = url_base_class_formatted[1]
                url_cloud_class = url_response[3]
                url_cloud_class_formatted = url_cloud_class.split(" ")
                url_cloud_response = url_cloud_class_formatted[1]
                print url + "," + url_base_class_response + "," + url_cloud_response


if __name__ == '__main__':
    check_urls()


