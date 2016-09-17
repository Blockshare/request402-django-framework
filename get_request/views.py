from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

from get_request.settings import CERTLY_API
from get_request.settings import FULLCONTACT_API

import ssl, socket
import OpenSSL
import json
import requests
import urllib.request as my_request


def index(request):
    #return render(request, '../templates/use_this_for_now.html', status=200)
    return render(request, '../templates/index.html', status=200)

# General overview of how the app can be used with instructions on how to provide the correct URL.
@api_view(['GET'])
@payment.required(0)
def info(request):
    get_info_border = '-------------------------------------------------------------------------------------------'
    get_status_info = '\nAll endpoints cost 2500 satoshi. \nReturns a websites HTTP status: 21 buy https://www.request402.org/get_status?uri=example.com\n'
    get_ip_info = 'Returns a websites IP: 21 buy https://www.request402.org/get_ip?uri=example.com\n'
    get_get = 'Returns GET data: 21 buy https://www.request402.org/get'
    get_ipinfo = 'Returns origin IP data: 21 buy https://www.request402.org/ipinfo\n'
    return HttpResponse("%s\nYou can easily use request402 by running any of the following commands:\n %s%s%s\n%s%s\n" \
                         % (get_info_border, get_status_info, get_ip_info, get_get, get_ipinfo, get_info_border), status=200)


# Get the header and status code from a website. Output in JSON.
@api_view(['GET'])
@payment.required(100)
def get_status(request):

    # Get the website url and assign it to variable url. 
    website_url = request.GET.get('url')
    url = 'http://'+website_url

    certify = requests.get('https://api.certly.io/v1/lookup?url='+url+'&token='+CERTLY_API).json()['data'][0]['status']

    # Open url, get the status code and headers and assign each to json output.
    try:
        response = my_request.urlopen(url)
        headers = response.getheaders()[0:8]
        message = {'status': {response.status : response.reason, 'trust': certify}, 'headers': {headers[0][0]: headers[0][1], \
                   headers[1][0]: headers[1][1], headers[2][0]: headers[2][1], \
                   headers[3][0]: headers[3][1], headers[4][0]: headers[4][1], \
                   headers[5][0]: headers[5][1]}}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    except:
        exception = {"exception raised" : "possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))



# Get the IP address of a website. Output in JSON
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
        exception = {"excpetion raised" : "possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))




# Get the IP address of user. Output in JSON
@api_view(['GET'])
@payment.required(100)
def ip(request):
    
    # IP address information from Django's 'request.META.get' command.
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    try:
        ip = x_forwarded_for.split(',')[0]
        message = {'origin': ip}
        return HttpResponse("Payment Required", json.dumps(message, indent=2), status=200)
    except:
        ip = request.META.get('REMOTE_ADDR')
        message = {'origin': ip}
        return render("Payment Required", json.dumps(message, indent=2), status=200)




# Returns the GET Header data. Output is JSON
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
        response = {'headers': {'Accept': accept, 'Encoding': encoding, 'User-Agent': agent, \
                    'HTTP-Host': host, 'args': args}, 'origin': origin}
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception))




# Get JSON-encoded output of a Bitcoin wallet address
@api_view(['GET'])
@payment.required(100)
def address(request):

    # Assign a wallet address to a variable, place in API url, and return as JSON.
    addr = request.GET.get('address')
    response = requests.get('https://api.blockcypher.com/v1/btc/main/addrs/' + addr)
    
    data = response.json()

    # Assign JSON output to variables.
    address = data['address']
    balance = data['balance'] / 100000000.0
    fnl_balance = data['final_balance'] / 100000000.0
    total_rec = data['total_received'] / 100000000.0
    total_sent = data['total_sent'] / 100000000.0

    # Return JSON-encoded output of variables.
    try:
        address_json = {'Bitcoin': {'balance': balance,'final_balance': fnl_balance, \
                        'total_received': total_rec, 'total_sent': total_sent}, 'address': address}
        return HttpResponse(json.dumps(address_json, indent=2), status=200)
    except:
        exception = {"Exception": "%s may not be a proper bitcoin address" % (address)}
        return HttpResponse(json.dumps(exception))




# Output all JSON-encoded IP information.    
@api_view(['GET'])
@payment.required(100)
def server_info(request):
    
    # Grab and assign URL information to JSON-encoded file.
    data = request.GET.get('uri')
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
        response = {'headers': {'accept': accept, 'encoding': encoding, \
                    'User-Agent': agent}, 'server': data}
        return HttpResponse(json.dumps(response, indent=2), status=200)
    except:
        exception = {"Exception": "Something isn't working correctly here."}
        return HttpResponse(json.dumps(exception), status=200)



@api_view(['GET'])
@payment.required(100)
def company_information(request):
    
    company = request.GET.get('url')

    response = requests.get('https://api.fullcontact.com/v2/company/lookup.json?domain='+company+'&apiKey='+FULLCONTACT_API)
    response = response.json()

    # Using exception handlers
    try:
        params = {
            'company-information': {
                'founded': response['organization']['founded'],
                'contact': response['organization']['contactInfo'],
            }
        }
        return HttpResponse(json.dumps(params, indent=2), status=200)        
    except:
        params = {"Exception Error": "It appears something broke in the code."}
        return HttpResponse(json.dumps(params, indent=2), status=200)


@api_view(['GET'])
@payment.required(100)
def twitter_search(request):

    username = request.GET.get('username')

    response = requests.get('https://api.fullcontact.com/v2/person.json?twitter='+username+'&apiKey='+FULLCONTACT_API)
    response = response.json()

    # Using exception handlers to handle logic.
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


@api_view(['GET'])
@payment.required(1000)
def get_ssl(request):

    url = request.GET.get('url')
    ssl_cert = ssl.get_server_certificate((url, 443))

    try:
        return HttpResponse("\n"+ssl_cert, status=200)
    except:
        return HttpResponse(("There doesn't seem to be a SSL certificate for the URL you provided."), status=200)


