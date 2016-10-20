"""
Copyright Blockshare Technologies, LLC.

"""

__author__ = "Casey O'Neill"
__version__ = "1.0"
__maintainer__ = "Casey O'Neill"
__email__ = "cpo@request402.com"

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


def index(request):
    """
    Returns landing home page.
    """
    return render(request, '../templates/index.html', status=200)


def info(request):
    """
    Returns landing info page.
    """
    return render(request, '../templates/info.html', status=200)


def get_moocher_baddomain_api(request):
    """
    Abstracting the moocher api call into its own function for simplicity.
    returns JSON-encoded output of a 'baddomain'.
    """
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", 'http://api.moocher.io/baddomain/' + request, headers=headers)
    return response.json()


@api_view(['GET'])
@payment.required(1000)
def get_status(request):
    """
    Input: Domain name URL.
    Output: JSON-encoded header and status code from url.
            {'status': {'is-trustworthy': ___, 'status_code': ___}, 'headers': {___}}
    Exception: Exception raised if URL does not exist or is broken.
    """
    website_url = request.GET.get('url')
    url = 'http://' + website_url

    data = get_moocher_baddomain_api(website_url)
    data_json = data['response']['ip']['score']
    clean = "clean" if data_json == 0 else "blacklist" 

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


@api_view(['GET'])
@payment.required(250)
def get_ip(request):
    """
    Input: Domain name URL.
    Output: JSON-encoded IP address of domain name url.
            {'domain-ip': {'origin': ___, 'url': ___}}
    Exception: Exception raised if URL does not exist or is broken.
    """
    url = request.GET.get('url')

    try:
        response = socket.gethostbyname(url)
        message = {'domain_ip': {'origin': response, 'url': url}}
        data = json.dumps(message, indent=2)
        return HttpResponse(data, status=200)
    except:
        exception = {"excpetion raised": "possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))


@api_view(['GET'])
@payment.required(5)
def ip(request):
    """
    Input: Run API URL in command line or call it via client script.
    Output: JSON-encoded IP address of users computer.
            {'origin': ___}
    Exception: Exception raised and 'REMOTE_ADDR' called.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    try:
        ip = x_forwarded_for.split(',')[0]
        message = {'origin': ip}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    except:
        ip = request.META.get('REMOTE_ADDR')
        message = {'origin': ip}
        return HttpsResponse(json.dumps(message, indent=2), status=200)


@api_view(['GET'])
@payment.required(100)
def get(request):
    """
    Input: Run API URL in command line or call it via client script.
    Output: JSON-encoded GET Header data.
            {'headers': {'Accept': ___, 'Encoding': ___, 'User-Agent': ___,
                        'HTTP-Host': ___, 'args': ___}, 'origin': ___}
    Exception: Exception raised with wrong url.
    """
    args = request.GET.get('args')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    http_accept = request.META.get('HTTP_ACCEPT')
    http_encoding = request.META.get('HTTP_ACCEPT_ENCODING')
    http_user_agent = request.META.get('HTTP_USER_AGENT')
    http_host = request.META.get('HTTP_HOST')

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


@api_view(['GET'])
@payment.required(100)
def address(request):
    """
    Input: Bitcoin wallet address.
    Output: JSON-encoded results of wallet address.
            {'Bitcoin': {'balance': ___, 'final_balance': ___,
                         'total_received': ___, 'total_sent': ___}, 'address': ___}
    Exception: Exception return if address not Bitcoin address.
    """
    addr = request.GET.get('address')
    response = requests.get(
        'https://api.blockcypher.com/v1/btc/main/addrs/' + addr)
    data = response.json()

    address = data['address']
    balance = data['balance'] / 100000000.0
    fnl_balance = data['final_balance'] / 100000000.0
    total_rec = data['total_received'] / 100000000.0
    total_sent = data['total_sent'] / 100000000.0

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
