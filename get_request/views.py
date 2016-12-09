"""
Copyright Blockshare Technologies, LLC.
  ____  _            _     ____  _                      ___ ___  
 | __ )| | ___   ___| | __/ ___|| |__   __ _ _ __ ___  |_ _/ _ \ 
 |  _ \| |/ _ \ / __| |/ /\___ \| '_ \ / _` | '__/ _ \  | | | | |
 | |_) | | (_) | (__|   <  ___) | | | | (_| | | |  __/_ | | |_| |
 |____/|_|\___/ \___|_|\_\|____/|_| |_|\__,_|_|  \___(_)___\___/ 


"""

__author__ = "cponeill"
__version__ = "1.0"
__maintainer__ = "cponeill"
__email__ = "cponeill@blockshare.io"

import ssl
import socket
import json
import requests
import urllib.request as my_request

from django.http import HttpResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse

from rest_framework.decorators import api_view
from two1.bitserv.django import payment
from xml.etree import ElementTree
from get_request.settings import MASHAPE
from get_request.settings import JSONWHOIS


def index(request):
    """Returns landing home page."""
    return render(request, '../templates/index.html', status=200)


def info(request):
    """Returns landing info page."""
    return render(request, '../templates/info.html', status=200)


def get_moocher_baddomain_api(request):
    """
    Abstracting the moocher api call into its own function.
    returns JSON-encoded output of a 'baddomain'.
    """
    headers = {'content-type': 'application/json'}
    response = requests.request("GET", 'http://api.moocher.io/baddomain/' + request, headers=headers)
    return response.json()


def get_domainr_api(request):
    """
    Abstracting the Domainr api call into its own function.
    returns JSON-encoded output of possible domain name.
    """
    api_url = 'https://domainr.p.mashape.com/v1/info?mashape-key='
    headers = {"X-Mashape-Key": MASHAPE, "Accept": "application/json"}
    response = requests.get(api_url + MASHAPE + '&q=' + request, headers=headers)
    return response.json()


def get_whois_api(request, endpoint):
    """
    Abstractin the jsonwhois api call into its own function.
    returns JSON-encoded output of domain name information
    """
    headers = {"Accept": "application/json", "Authorization": "Token token=" + JSONWHOIS}
    params = {"domain": request}
    response = requests.get("https://jsonwhois.com/api/v1/" + endpoint, headers=headers, params=params)
    return response.json()


def get_alexa_xml(request):
    """
    Abstracting Alexa rankins into its own function.
    Returns XML output. This output will then be turned into JSON.
    """
    response = requests.get('http://data.alexa.com/data?cli=10&url=http://' + request)
    tree = ElementTree.fromstring(response.text)
    return tree   


@api_view(['GET'])
@payment.required(1000)
def get_status(request):
    """
    Input: Domain name URL.
    Output: JSON-encoded header and status code from url.
            {'status': {'trustworthy': ___, 'status_code': ___}, 'headers': {___}}
    Exception: Exception raised if URL does not exist or is broken.
    """
    website_url = request.GET.get('url')
    url = 'http://' + website_url

    data = get_moocher_baddomain_api(website_url)
    data_json = data['response']['ip']['score']
    clean = "yes" if data_json == 0 else "blacklisted" 

    try:
        response = my_request.urlopen(url)
        headers = response.getheaders()[0:8]
        message = {
            'status': {
                response.status: response.reason,
                'trustworthy': clean
            }, 
            'headers': {
                 headers[0][0]: headers[0][1],
                 headers[1][0]: headers[1][1],
                 headers[2][0]: headers[2][1],
                 headers[3][0]: headers[3][1],
                 headers[4][0]: headers[4][1],
                 headers[5][0]: headers[5][1]
            }
        }
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
        return HttpResponse(json.dumps(message, indent=2), status=200)


@api_view(['GET'])
@payment.required(5)
def get(request):
    """
    Input: Run API URL in command line or call it via client script.
    Output: JSON-encoded GET Header data.
            {'headers': {'Accept': ___, 'Encoding': ___, 'User-Agent': ___,
                        'HTTP-Host': ___}, 'origin': ___}
    Exception: Exception raised with wrong url.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    http_accept = request.META.get('HTTP_ACCEPT')
    http_encoding = request.META.get('HTTP_ACCEPT_ENCODING')
    http_user_agent = request.META.get('HTTP_USER_AGENT')
    http_host = request.META.get('HTTP_HOST')
    http_connect = request.META.get('HTTP_CONNECTION')    

    try:
        origin = x_forwarded_for.split(',')[0]
        accept = http_accept.split(',')[0]
        encoding = http_encoding.split(',')[0]
        agent = http_user_agent.split(',')[0]
        host = http_host.split(',')[0]
        connect = http_connect.split(',')[0]
        response = {
            'headers': {
                'Accept': accept,
                'Encoding': encoding,
                'User-Agent': agent,
                'HTTP-Host': host,
                'Connection': connect,
            },
            'origin': origin
        }
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception))



@api_view(['GET'])
@payment.required(5)
def server_info(request):
    """
    Input: Domain name URL.
    Output: JSON-encoded server location information.
    Exception raised if domain not correct or available.
    """
    data = request.GET.get('url')
    uri = 'http://ipinfo.io'
    raw = requests.get(uri)
    data = raw.json()

    http_accept = request.META.get('HTTP_ACCEPT')
    http_encoding = request.META.get('HTTP_ACCEPT_ENCODING')
    http_user_agent = request.META.get('HTTP_USER_AGENT')

    try:
        accept = http_accept.split(',')[0]
        encoding = http_encoding.split(',')[0]
        agent = http_user_agent.split(',')[0]
        response = {
            'headers': {
                'accept': accept,
                'encoding': encoding,
                'User-Agent': agent
            },
            'server': data
        }
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception), status=200)


@api_view(['GET'])
@payment.required(1000)
def get_ssl(request):
    """
    Input: TLS/SSL certified URL.
    Output: The public key of the URL's SSL certificate.
    Exception raised if domain not TLS/SSL certified.
    """
    url = request.GET.get('url')
    ssl_cert = ssl.get_server_certificate((url, 443))

    try:
        return HttpResponse("\n" + ssl_cert, status=200)
    except:
        return HttpResponse(("There doesn't seem to be a SSL certificate for the URL you provided."), status=200)


@api_view(['GET'])
@payment.required(2500)
def get_ssl_source(request):
    """
    Input: TLS/SSL certified URL.
    Output: JSON-encoded source information of an SSL certificate.
    Exception raised if domain not TLS/SSL certified.
    """
    hostname = request.GET.get('url')

    try:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
        s.connect((hostname, 443))
        cert = s.getpeercert()
        subject = dict(x[0] for x in cert['subject'])
        issuer = dict(x[0] for x in cert['issuer'])
        dns = [x[1] for x in cert['subjectAltName']]
        subject_list = {
            'ssl-info': {
                'org-info': subject,
                'serial-number': cert['serialNumber'],
                'certificate': cert['caIssuers'][0],
                'status-protocol': cert['OCSP'][0],
                'dns': dns,
                'issuer': issuer
            }
        }
        return HttpResponse(json.dumps(subject_list, indent=2), status=200)
    except:
        exception = {'exception error': 'either the hostname is not HTTPS it was typed incorrectly.'}
        return HttpResponse(json.dumps(exception, indent=2), status=200)


@api_view(['GET'])
@payment.required(1000)
def get_blacklist(request):
    """
    Input: Domain URL.
    Ouput: JSON-encoded information of trustworthiness of URL. 
    Exception raised if domain does not exist 
    """
    domain = request.GET.get('url')

    try:
        response = get_moocher_baddomain_api(domain)
        msg = {'baddomain-info': response}
        return HttpResponse(json.dumps(msg, indent=2), status=200)
    except:
        response = {'exception error': 'there seems to be something wrong with the request.'}
        return HttpResponse(json.dumps(response, indent=2), status=200)


@api_view(['GET'])
@payment.required(750)
def get_rank(request):
    """
    Input: Specific URL.
    Output: JSON-encoded Alexa rankings of URL.
    Exception raised if domain not found in rankings or does not rank high enough.
    """
    url = request.GET.get('url')

    try:
        rank = get_alexa_xml(url).find(".//REACH").get("RANK")
        delta = get_alexa_xml(url).find(".//RANK").get("DELTA")
        params = {
            'domain-rank': {
                'rank': rank,
                'rank-change': delta,
                'url': url
            }
        }
        return HttpResponse(json.dumps(params, indent=2), status=200)
    except:
        params = {'alexa-ranking': {'ranking': 'this domain is not ranked'}}
        return HttpResponse(json.dumps(params, indent=2), status=200)


@api_view(['GET'])
@payment.required(1000)
def domain_search(request):
    """
    Input: Domain name / URL.
    Output: JSON-encoded search suggestions related to the query, as well as availability
            and links to register the suggested domains
    Exception raised if domain not found.
    """
    url = request.GET.get('url')

    try:
        response = get_domainr_api(url)
        tld = response['tld']
        whois_url = response['whois_url']
        availability = response['availability']
        data = {
            'domain-search': {
                'tld-info': tld,
                'whois_url': whois_url,
                'availability': availability
            }
        }
        return HttpResponse(json.dumps(data, indent=2), status=200)
    except:
        data = {'exception': 'there might be something wrong with the url'}
        return HttpResponse(json.dumps(data, indent=2), status=200)


@api_view(['GET'])
@payment.required(1000)
def domain_social(request):
    """
    Input: Domain URL.
    Output: JSON-encoded social stats of website.
    Exception raised if domain or api not working correctly.
    """
    url = request.GET.get('url')

    try:
        response = get_whois_api(url, 'social')
        params = {'social-stats': response}
        return HttpResponse(json.dumps(params, indent=2), status=200)
    except:
        params = {'exception raised': 'there is a problem with the url.'}
        return HttpResponse(json.dumps(params, indent=2), status=200)


@api_view(['GET'])
@payment.required(2500)
def domain_screenshot(request):
    """
    Input: Domain URL.
    Output: JSON-encoded link to screenshot of website.
    Exception raised if domain or api not working correctly.
    """
    url = request.GET.get('url')
    
    try:
        response = get_whois_api(url, 'screenshot')
        params = {'screenshot': response}
        return HttpResponse(json.dumps(params, indent=2), status=200)
    except:
        params = {'exception raised': 'there is a problem with the url.'}
        return HttpResponse(json.dumps(params, indent=2), status=200)
