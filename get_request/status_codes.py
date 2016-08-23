def check_status(status):
	#2xx Success
	if status == 200:
		return ("OK")
	elif status == 201:
		return ("Created")
	elif status == 202:
		return ("Accepted")
	elif status == 203:
		return ("Non-Authoritative Information")
	elif status == 204:
		return ("No Content")
	elif status == 205:
		return ("Reset Content")
	elif status == 206:
		return ("Partial Content")
	elif status == 207:
		return ("Multi-Status")
	elif status == 208:
		return ("Already Reported")
	elif status == 226:
		return ("IM Used")

	#3xx Redirection
	elif status == 300:
		return ("Multiple Choices")
	elif status == 301:
		return ("Moved Permanently")
	elif status == 302:
		return ("Found")
	elif status == 303:
		return ("See Other")
	elif status == 304:
		return ("Not Modified")
	elif status == 305:
		return ("Use Proxy")
	elif status == 306:
		return ("Switch Proxy")
	elif status == 307:
		return ("Temporary Redirect")
	elif status == 308:
		return ("Permanent Redirect")

	#4xx Client Error
	elif status == 400:
		return ("Bad Request")
	elif status == 401:
		return ("Unauthorized")
	elif status == 402:
		return ("Payment Required")
	elif status == 403:
		return ("Forbidden")
	elif status == 404:
		return ("Not Found")
	elif status == 405:
		return ("Method Not Allowed")
	elif status == 406:
		return ("Not Acceptable")
	elif status == 407:
		return ("Proxy Authentication Required")
	elif status == 408:
		return ("Request Timeout")
	elif status == 409:
		return ("Conflict")
	elif status == 410:
		return ("Gone")
	elif status == 411:
		return ("Length Required")
	elif status == 412:
		return ("Precondition Failed")
	elif status == 413:
		return ("Payload Too Large")
	elif status == 414:
		return ("URI Too Long")
	elif status == 415:
		return ("Unsupported Media Type")
	elif status == 416:
		return ("Range Not Satisfiable")
	elif status == 417:
		return ("Expectation Failed")
	elif status == 418:
		return ("I'm a teapot")
	elif status == 421:
		return ("Misdirected Request")
	elif status == 422:
		return ("Unprocessable Entity")
	elif status == 423:
		return ("Locked")
	elif status == 424:
		return ("Failed Dependency")
	elif status == 426:
		return ("Upgrade Required")
	elif status == 428:
		return ("Precondition Required")
	elif status == 429:
		return ("Too Many Requests")
	elif status == 431:
		return ("Request Header Fields Too Large")
	elif status == 451:
		return ("Unavailable For Legal Reasons")

	elif status == 440:
		return ("Login Timeout")
	elif status == 449:
		return ("Retry With")

	#5xx Server Error
	elif status == 500:
		return ("Internal Server Error")
	elif status == 501:
		return ("Not Implemented")
	elif status == 502:
		return ("Bad Gateway")
	elif status == 503:
		return ("Service Unavailable")
	elif status == 504:
		return ("Gateway Timeout")
	elif status == 505:
		return ("HTTP Version Not Supported")
	elif status == 506:
		return ("Variant Also Negotiates")
	elif status == 507:
		return ("Insufficient Storage")
	elif status == 508:
		return ("Loop Detected")
	elif status == 510:
		return ("Not Extended")
	elif status == 511:
		return ("Network Authentication Required")

	#Unofficial codes
	elif status == 103:
		return ("Checkpoint")
	elif status == 450:
		return ("Blocked by Windows Parental Controls")
	elif status == 509:
		return ("Bandwidth Limit Exceeded")

	#nginx
	elif status == 444:
		return ("No Response (nginx)")
	elif status == 495:
		return ("SSL Certificate Error (nginx)")
	elif status == 496:
		return ("SSL Certificate Required (nginx)")
	elif status == 497:
		return ("HTTP Request Sent to HTTPS Port (nginx)")
	elif status == 499:
		return ("Client Closed Request (nginx)")

	#CloudFlare
	elif status == 520:
		return ("Unknown Error (CloudFlare)")
	elif status == 521:
		return ("Web Server Is Down (CloudFlare)")
	elif status == 522:
		return ("Connection Timed Out (CloudFlare)")
	elif status == 523:
		return ("Origin Is Unreachable (CloudFlare)")
	elif status == 524:
		return ("A Timeout Occurred (CloudFlare)")
	elif status == 525:
		return ("SSL Handshake Failed (CloudFlare)")
	elif status == 526:
		return ("Invalid SSL Certificate (CloudFlare)")
