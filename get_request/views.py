from django.http import HttpResponse

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

import socket
import json
import requests
import urllib.request as my_request


# General overview of how the app can be used with instructions on how to provide the correct URL.
@api_view(['GET'])
@payment.required(0)
def info(request):
    get_info_border = '-------------------------------------------------------------------------------------------'
    get_status_info = '\nReturns a websites HTTP status: 21 buy https://www.request402.org/get_status?uri=example.com\n'
    get_ip_info = 'Returns a websites IP: 21 buy https://www.request402.org/get_ip?uri=example.com\n'
    get_ip = 'Returns origin IP: 21 buy https://www.request402.org/ip\n'
    get_get = 'Returns GET data: 21 buy https://www.request402.org/get'
    return HttpResponse("%s\nYou can easily use request402 by running any of the following commands:\n %s%s%s\n%s%s\n" \
                         % (get_info_border, get_status_info, get_ip_info, get_get, get_ip, get_info_border), status=200)

# Get the header and status code from a website. Output in JSON.
@api_view(['GET'])
@payment.required(10)
def get_status(request):

    """
    Function calls a website url and returns json output of headers and status code.

    Input: => https://www.request402.org/get_status?url=example.com
    Output: => JSON {status, headers}
    """
    
    # Get the website url and assign it to variable url. 
    website_url = request.GET.get('uri')
    url = 'http://'+website_url


    # Open url, get the status code and headers and assign each to json output.
    try:
        response = my_request.urlopen(url)
        headers = response.getheaders()[0:8]
        message = {'Status': {response.status : response.reason}, 'Headers': {headers[0][0]: headers[0][1], \
                   headers[1][0]: headers[1][1], headers[2][0]: headers[2][1], \
                   headers[3][0]: headers[3][1], headers[4][0]: headers[4][1], \
                   headers[5][0]: headers[5][1]}}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    except:
        exception = {"Exception raised" : "Possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))

# Get the IP address of a website. Output in JSON
@api_view(['GET'])
@payment.required(10)
def get_ip(request):
    # Add function description comment code.    
    url = request.GET.get('uri')
    
    try:
        response = socket.gethostbyname(url)
        message = {'IP_Info': {'Origin': response, 'Url': url}}
        data = json.dumps(message, indent=2)
        return HttpResponse(data, status=200)
    except:
        exception = {"Excpetion raised" : "Possible %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))

# Get the IP address of user. Output in JSON
@api_view(['GET'])
@payment.required(10)
def ip(request):
    # Add Comment code for input and Output
    # Change from "if-else" conditional to "try-except".
    """
    Input: => /ip
    Output: => JSON-encoded output of IP origin and URL.
    ex: {"origin": ip_address, "url", "url}

    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        message = {'Origin': ip}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    else:
        ip = request.META.get('REMOTE_ADDR')
        message = {'Origin': ip}
        return HttpResponse(json.dumps(message, indent=2), status=200)


# Returns the GET Header data. Output is JSON
@api_view(['GET'])
@payment.required(10)
def get(request):

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
        response = {'Headers': {'Accept': accept, 'Encoding': encoding, 'User-Agent': agent, \
                    'HTTP-Host': host}, 'Origin': origin}
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception))


# Get JSON-encoded output of a Bitcoin wallet address
@api_view(['GET'])
@payment.required(1000)
def address(request):
    """
    Returns JSON-encoded output of Bitcoin wallet address information.

    Input: => /bitcoin?address=<address>
    Output: => {'variable': response}

    """

    addr = request.GET.get('address')
    response = requests.get('https://api.blockcypher.com/v1/btc/main/addrs/' + addr)
    
    data = response.json()

    address = data['address']
    balance = data['balance'] / 100000000.0
    fnl_balance = data['final_balance'] / 100000000.0
    total_rec = data['total_received'] / 100000000.0
    total_sent = data['total_sent'] / 100000000.0

    try:
        address_json = {'Bitcoin': {'balance': balance,'final_balance': fnl_balance, \
                        'total_received': total_rec, 'total_sent': total_sent}, 'address': address}
        return HttpResponse(json.dumps(address_json, indent=2), status=200)
    except:
        exception = {"Exception": "%s may not be a proper bitcoin address" % (address)}
        return HttpResponse(json.dumps(exception))
    
