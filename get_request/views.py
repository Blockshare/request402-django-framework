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
    get_status_info = '\nReturns a websites HTTP status: 21 buy http://www.request402.org/get_status?url=example.com\n'
    get_ip_info = 'Returns a websites IP: 21 buy http://www.request402.org/get_ip?url=example.com\n'
    get_ip = 'Returns origin IP: 21 buy http://www.request402.org/ip'
    return HttpResponse("%s\nYou can easily use request402 by running any of the following commands:\n %s%s%s\n%s\n" % (get_info_border, get_status_info, get_ip_info, get_ip, get_info_border), status=200)

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
        status = response.getcode()
        description = check_status(status)
        headers = response.getheaders()[0:8]
        message = {status : description, 'Headers': {headers[0][0]: headers[0][1], \
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
        message = {'Origin': response, 'Url': url}
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
# Will work on this for deployment once the application is deployed.
@api_view(['GET'])
@payment.required(10)
def get(request):

    return HttpResponse('Soon...', status=200)
    """
    http_accept = request.META.get('HTTP_ACCEPT')
    http_accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING')
    http_user_agent = request.META.get('HTTP_USER_AGENT')
    content_length = request.META.get('CONTENT_LENGTH')
    content_type = request.META.get('CONTENT_TYPE')
    server_name = request.META.get('SERVER_NAME')
    http_host = request.META.get('HTTP_HOST')
    http_remote_host = request.META.get('REMOTE_HOST')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')


    if http_accept:
        accept = http_accept.split(',')[0]
        encoding = http_accept_encoding.split(',')[0]
        content = content_type.split(',')[0]
        length = content_length.split(',')[0]
        agent = http_user_agent.split(',')[0]
        server = server_name.split(',')[0]
        host = http_host.split(',')[0]
        remote_host = http_remote_host.split(',')[0]
        message = {'Headers': {'Encoding': encoding}}
        #message = {'Headers': {'Accept': accept, 'Encoding': encoding, 'User-Agent': agent,\
                   #'Content-Type': content, 'Content-Length': length, 'Server-Name': server,\
                   #'Host': host, 'Remote-Host': remote_host}}
        return HttpResponse(json.dumps(message, indent=2), status=200)
    else:
        return HttpResponse('NOPE', status=200)

    """
