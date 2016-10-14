from django.http import HttpResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from get_request.settings import FULLCONTACT_API

import ssl
import socket
import json
import requests
import shutil
import subprocess
import sys
import urllib.request as my_request

# Function that returns the landing home page.
def index(request):
    return render(request, '../templates/index.html', status=200)

# Function that returns the info landing page.
def info(request):
    return render(request, '../templates/info.html', status=200)


def get_moocher_baddomain_api(request):
    """
    Abstracting the moocher api call into its own function for simplicity.
    returns JSON-encoded output of a 'baddomain'.
    """
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", 'http://api.moocher.io/baddomain/' + request, headers=headers)
    return response.json()

# Get JSON-encoded header and status code from a website.
@api_view(['GET'])
@payment.required(100)
def get_status(request):

    # Get the website url and assign it to variable url.
    website_url = request.GET.get('url')
    url = 'http://' + website_url

    data = get_moocher_baddomain_api(website_url)
    data_json = data['response']['ip']['score']
    clean = "clean" if data_json == 0 else "blacklist" 

    # Open url, get the status code and headers and assign each to json output.
    try:
        response = my_request.urlopen(url)
        headers = response.getheaders()[0:8]
        message = {'status': {response.status: response.reason, 'is-trustworthy': clean},
                   'headers': {headers[0][0]: headers[0][1], headers[1][0]: headers[1][1],
                               headers[2][0]: headers[2][1], headers[3][0]: headers[3][1],
                               headers[4][0]: headers[4][1], headers[5][0]: headers[5][1]}}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    except:
        exception = {"exception raised": "possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))


# Get JSON-encoded IP address of a website.
@api_view(['GET'])
@payment.required(100)
def get_ip(request):

    # grab the url for the IP address.
    url = request.GET.get('url')

    # Assign url and IP to variables and return them as JSON-encoded output.
    try:
        response = socket.gethostbyname(url)
        message = {'domain_ip': {'origin': response, 'url': url}}
        data = json.dumps(message, indent=2)
        return HttpResponse(data, status=200)
    except:
        exception = {"excpetion raised": "possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))


# Get JSON-encoded IP address of user.
@api_view(['GET'])
@payment.required(100)
def ip(request):

    # IP address information from Django's 'request.META.get' command.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    try:
        ip = x_forwarded_for.split(',')[0]
        message = {'origin': ip}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    except:
        ip = request.META.get('REMOTE_ADDR')
        message = {'origin': ip}
        return HttpsResponse(json.dumps(message, indent=2), status=200)


# Returns JSON-encoded GET Header data.
@api_view(['GET'])
@payment.required(100)
def get(request):

    # Grab and arguments as a string.
    args = request.GET.get('args')

    # Grab Header information using Djangos request.META.get command.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    http_accept = request.META.get('HTTP_ACCEPT')
    http_encoding = request.META.get('HTTP_ACCEPT_ENCODING')
    http_user_agent = request.META.get('HTTP_USER_AGENT')
    http_host = request.META.get('HTTP_HOST')

    # Assign Header information to variables and return as JSON-encoded output.
    try:
        origin = x_forwarded_for.split(',')[0]
        accept = http_accept.split(',')[0]
        encoding = http_encoding.split(',')[0]
        agent = http_user_agent.split(',')[0]
        host = http_host.split(',')[0]
        response = {'headers': {'Accept': accept, 'Encoding': encoding, 'User-Agent': agent,
                                'HTTP-Host': host, 'args': args}, 'origin': origin}
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception))


# Get JSON-encoded output of a Bitcoin wallet address.
@api_view(['GET'])
@payment.required(100)
def address(request):

    # Assign a wallet address to a variable, place in API url, and return as
    # JSON.
    addr = request.GET.get('address')
    response = requests.get(
        'https://api.blockcypher.com/v1/btc/main/addrs/' + addr)
    data = response.json()

    # Assign JSON output to variables.
    address = data['address']
    balance = data['balance'] / 100000000.0
    fnl_balance = data['final_balance'] / 100000000.0
    total_rec = data['total_received'] / 100000000.0
    total_sent = data['total_sent'] / 100000000.0

    # Return JSON-encoded output of variables.
    try:
        address_json = {'Bitcoin': {'balance': balance, 'final_balance': fnl_balance,
                                    'total_received': total_rec, 'total_sent': total_sent}, 'address': address}
        return HttpResponse(json.dumps(address_json, indent=2), status=200)
    except:
        exception = {
            "exception": "%s may not be a proper bitcoin address" % (address)}
        return HttpResponse(json.dumps(exception))


# Output all JSON-encoded server location information.
@api_view(['GET'])
@payment.required(100)
def server_info(request):

    # Grab and assign URL information to JSON-encoded file.
    data = request.GET.get('url')
    uri = 'http://ipinfo.io'
    raw = requests.get(uri)
    data = raw.json()

    # Grab and assign Header information from Django request.META.get command.
    http_accept = request.META.get('HTTP_ACCEPT')
    http_encoding = request.META.get('HTTP_ACCEPT_ENCODING')
    http_user_agent = request.META.get('HTTP_USER_AGENT')

    # Combine variables and return all as JSON-encoded output.
    try:
        accept = http_accept.split(',')[0]
        encoding = http_encoding.split(',')[0]
        agent = http_user_agent.split(',')[0]
        response = {'headers': {'accept': accept, 'encoding': encoding,
                                'User-Agent': agent}, 'server': data}
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception), status=200)


# Get JSON-encoded output of company contact information from url.
@api_view(['GET'])
@payment.required(100)
def company_information(request):

    # Get url and assign to 'response' variable and output as JSON.
    company = request.GET.get('url')
    response = requests.get(
        'https://api.fullcontact.com/v2/company/lookup.json?domain=' + company + '&apiKey=' + FULLCONTACT_API)
    response = response.json()

    # Assign variable output to new JSON dict and return params. Break if
    # there is an error.
    try:
        params = {
            'company-information': {
                'founded': response['organization']['founded'],
                'contact': response['organization']['contactInfo'],
            }
        }
        return HttpResponse(json.dumps(params, indent=2), status=200)
    except:
        params = {"exception error": "it appears something broke in the code."}
        return HttpResponse(json.dumps(params, indent=2), status=200)


# Get JSON-encoded output of twitter username search.
@api_view(['GET'])
@payment.required(100)
def twitter_search(request):

    # Get username, assign to variable, call 'fullcontact' api, and return
    # json.
    username = request.GET.get('username')
    response = requests.get(
        'https://api.fullcontact.com/v2/person.json?twitter=' + username + '&apiKey=' + FULLCONTACT_API)
    response = response.json()

    # Assign variable output to new JSON dict and return params. Break if
    # there is an error.
    try:
        params = {
            'user_info': {
                'demographics': response['demographics'],
                'social_profiles': response['socialProfiles']
            }
        }
        return HttpResponse(json.dumps(params, indent=2), status=200)
    except:
        params = {"Exception Error": "It appears something broke in the code."}
        return HttpResponse(json.dumps(params, indent=2), status=200)


# Get the public key of an URL's SSL certificate.
@api_view(['GET'])
@payment.required(1000)
def get_ssl(request):

    # Get url and assign to variable that is fetching whether or not there is
    # a SSL certificate for that url.
    url = request.GET.get('url')
    ssl_cert = ssl.get_server_certificate((url, 443))

    # Return public key SSL certificate if it is available. Break if there is
    # an error.
    try:
        return HttpResponse("\n" + ssl_cert, status=200)
    except:
        return HttpResponse(("There doesn't seem to be a SSL certificate for the URL you provided."), status=200)


# Get the source of an SSL certificate.
# Add comments code about this function.	
@api_view(['GET'])
@payment.required(2500)
def get_ssl_source(request):

    hostname = request.GET.get('url')

    try:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
        s.connect((hostname, 443))
        cert = s.getpeercert()
        subject = dict(x[0] for x in cert['subject'])
        issuer = dict(x[0] for x in cert['issuer'])
        dns = [x[1] for x in cert['subjectAltName']]
        subject_list = {'ssl-info': {'org-info': subject, 'serial-number': cert['serialNumber'], 'certificate': cert['caIssuers'][0], \
                     'status-protocol': cert['OCSP'][0], 'dns': dns, 'issuer': issuer}}
        return HttpResponse(json.dumps(subject_list, indent=2), status=200)
    except:
        exception = {'exception error': 'either the hostname is not HTTPS it was typed incorrectly.'}
        return HttpResponse(json.dumps(exception, indent=2), status=200)


@api_view(['GET'])
@payment.required(1000)
def get_blacklist(request):

    domain = request.GET.get('url')

    try:
        response = get_moocher_baddomain_api(domain)
        msg = {'baddomain-info': response}
        return HttpResponse(json.dumps(msg, indent=2), status=200)
    except:
        response = {'exception error': 'there seems to be something wrong with the request.'}
        return HttpResponse(json.dumps(response, indent=2), status=200)


@api_view(['GET'])
@payment.required(5)
def ping(request):

    url = request.GET.get('url')

    try:
        out = subprocess.check_output(['ping', '-c', str(6),
            '-s', str(64), '-W', str(3.0), str(url)]
        ).decode('unicode_escape')
    except subprocess.CalledProcessError:
        raise ValueError("ping cannot be performed on url={}".format(url))
    ping = [line for line in out.split('\n') if line != '']

    ip = socket.gethostbyname(url)

    info = {'ping-info': {'ping': ping,'ip': ip}}

    try:
        return HttpResponse(json.dumps(info, indent=2), status=200)
    except:
        exception = {'exception error': 'trace not working properly.'}
        return HttpResponse(json.dumps(exception, indent=2), status=200)
