# request402: 
HTTP Request & Response Micropayments Service
===========================================
![Blockshare](https://machine-payable.herokuapp.com/static/img/abstractdot.ico)

Request the IP address, Headers, and Status Code of any website.

<h3> Basic Requirements </h3>

1. A  <a href="https://21.co">21 Bitcoin Computer</a> or 21 installed.
2. You will need to be connected the 21 Zerotier Marketplace.

How to use:

    $ 21 buy https://www.request402.org/get_status?url=www.example.com -> Status and Headers
    $ 21 buy https://www.request402.org/get_ip?url=www.example.com --> IP Address
    $ 21 buy https://www.request402.org/ip --> User IP Address


<p>Here is an example of the JSON response when running /get_status?url=www.example.com for Google</p>
<pre><code> {
    "200": "OK",
    "headers": [
        [
            "Date",
            "Mon, 22 Aug 2016 17:29:27 GMT"
        ],
        [
            "Expires",
            "-1"
        ],
        [
            "Cache-Control",
            "private, max-age=0"
        ],
        [
            "Content-Type",
            "text/html; charset=ISO-8859-1"
        ],
        [
            "P3P",
            "CP=\"This is not a P3P policy! See https://www.google.com/support/accounts/answer/151657?hl=en for more info.\""
        ],
        [
            "Server",
            "gws"
        ],
        [
            "X-XSS-Protection",
            "1; mode=block"
        ],
        [
            "X-Frame-Options",
            "SAMEORIGIN"
        ]
    ]
}

</code></pre>
<p>This is an example of runnng /get_ip?url=www.example.com for Google.</p>
<pre><code>{
    "origin": "216.58.219.164",
    "url": "www.google.com"
}
</code></pre>

<p>This is an example of running /ip </p>
<pre><code>{
    "origin": 172.217.4.78
}
</code></pre>
