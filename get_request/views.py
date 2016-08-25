from django.http import HttpResponse

from rest_framework.decorators import api_view
from two1.bitserv.django import payment

import socket
import json
import urllib.request as my_request


from get_request.status_codes import check_status

# General overview of how the app can be used with instructions on how to provide the correct URL.
@api_view(['GET'])
@payment.required(0)
def info(request):
    get_info_border = '-------------------------------------------------------------------------------------------'
    get_status_info = '\nCheck the HTTP status: 21 buy http://www.request402.org/get_status?url=example.com\n'
    get_ip_info = 'Check the IP address of a website: 21 buy http://www.request402.org/get_ip?url=example.com'
    return HttpResponse("%s\nYou can easily use request402 by running any of the following commands:\n %s%s\n%s\n" % (get_info_border, get_status_info, get_ip_info, get_info_border), status=200)

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
    website_url = request.GET.get('url')
    url = 'http://'+website_url

    # Open url, get the status code and headers and assign each to json output.
    try:
        response = my_request.urlopen(url)
        status = response.getcode()
        description = check_status(status)
        headers = response.getheaders()[0:8]
        message = {status : description, 'headers': headers}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    except:
        exception = {"Exception raised" : "Possibly %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))


# Get the IP address of a website. Output in JSON
@api_view(['GET'])
@payment.required(10)
def get_ip(request):
    # Add function description comment code.    
    url = request.GET.get('url')
    
    try:
        response = socket.gethostbyname(url)
        message = {'origin': response, 'url': url}
        data = json.dumps(message, indent=2)
        return HttpResponse(data, status=200)
    except:
        exception = {"Excpetion raised" : "Possible %s doesn't exist" % (url)}
        return HttpResponse(json.dumps(exception, indent=2))

# Get the IP address of user. Output in JSON
@api_view(['GET'])
@payment.required(10)
def ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        message = {'origin': ip}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    else:
        ip = request.META.get('REMOTE_ADDR')
        message = {'origin': ip}
        return HttpResponse(json.dumps(message, indent=2), status=200)
