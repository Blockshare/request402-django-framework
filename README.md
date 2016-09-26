# Request402:
HTTP Request & Response Micropayments Service
===========================================
![Blockshare](https://machine-payable.herokuapp.com/static/img/abstractdot.ico)

HTTP(S) Request & Response Micropayments Service

All endpoint responses are JSON-encoded and cost 2500 satoshis. This is about $0.015 at current exchange prices.
A quick reference text can be found by running https://www.request402.com/info


<h3> Basic Requirements </h3>

1. A  <a href="https://21.co">21 Bitcoin Computer</a> or 21 installed.
2. You will need to be connected the 21 Zerotier Marketplace.
3. Make sure you have mined or have enough satoshi in your wallet for transactions.

How to use:

    $ 21 buy https://www.request402.com/ip --> Get the origin of your IP address.
    $ 21 buy https://www.request402.com/get --> Return GET data.
    $ 21 buy https://www.request402.com/server-location --> Return header and server location data.
    $ 21 buy https://www.request402.com/domain_status --> Get the header, status, and trustworthiness of a specfic domain url.
    $ 21 buy https://www.request402.com/domain_ip --> Get the origin IP address of a specific domain url.
    $ 21 buy https://www.request402.com/ssl-cert --> Return public key of SSL certificate for verification.
    $ 21 buy https://www.request402.com/company-contact --> Return public key of SSL certificate for verification.
    $ 21 buy https://www.request402.com/twitter --> Return demographic and social media account information of a Twitter username.
    $ 21 buy https://www.request402.com/bitcoin?address=<wallet address> --> Wallet Address Information


<p>Here is an example of the JSON response when running /get_status?uri=www.example.com for Slack.</p>
<pre><code>{
    "headers": {
        "Content-Type": "text/html; charset=utf-8",
        "Date": "Fri, 26 Aug 2016 22:27:32 GMT",
        "Transfer-Encoding": "chunked",
        "Connection": "close",
        "Server": "Apache",
        "Content-Security-Policy": "referrer no-referrer;"
    },
    "status": {
        "trust": "clean",
        "200": "OK"
    }
}
</code></pre>
<p>This is an example of runnng /get_ip?uri=www.example.com for Google.</p>
<pre><code>{
    "ip_info": {
        "url": "google.com",
        "origin": "74.125.29.138"
    }
}
</code></pre>

<p>This is an example of running /ip </p>
<pre><code>{
    "origin": xxx.xxx.x.xx
}
</code></pre>
<p>This is an example running /get </p>
<pre><code>{
    "headers": {
        "args": null,
        "User-Agent": "xxxxxx",
        "HTTP-Host": "www.xxxxxx.com",
        "Accept": "*/*",
        "Encoding": "gzip"
    },
    "origin": "xxx.xxx.xx.xxx"
}
</code></pre>

<p>This is an example of running /bitcoin?address=<wallet address> for 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.</p>
<pre><code>{
    "Bitcoin": {
        "balance": 16.31927487,
        "total_sent": 0.0,
        "final_balance": 16.31927487,
        "total_received": 16.31927487
    },
    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
}
</code></pre>
<p>This is an example of running /server-location.</p>
<pre><code>{
    "headers": {
        "encoding": "gzip",
        "accept": "*/*",
        "User-Agent": "xxxxxx"
    },
    "server": {
        "loc": "xx,xx",
        "ip": "xx.xx.xx.xxx",
        "city": "Ashburn",
        "org": "AS14618 Amazon.com, Inc.",
        "hostname": "ec2-xx-xx-xx-xxx.compute-x.amazonaws.com",
        "region": "Virginia",
        "postal": "20149",
        "country": "US"
    }
}
</code></pre>
