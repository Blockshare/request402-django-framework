# request402: 
HTTP Request & Response Micropayments Service
===========================================
![Blockshare](https://machine-payable.herokuapp.com/static/img/abstractdot.ico)

Request the IP address, Headers, and Status Code of any website for micropayments. More endpoints are being considered.

All endpoint responses are JSON-encoded

<h3> Basic Requirements </h3>

1. A  <a href="https://21.co">21 Bitcoin Computer</a> or 21 installed.
2. You will need to be connected the 21 Zerotier Marketplace.

How to use:

    $ 21 buy https://www.request402.org/get_status?uri=<www.example.com> -> Status and Headers
    $ 21 buy https://www.request402.org/get_ip?uri=<www.example.com> --> IP Address
    $ 21 buy https://www.request402.org/ip --> User IP Address
    $ 21 buy https://www.request402.com/bitcoin?address=<wallet address> --> Wallet Addres Information


<p>Here is an example of the JSON response when running /get_status?uri=www.example.com for Slack.</p>
<pre><code>{
    "Headers": {
        "Content-Type": "text/html; charset=utf-8",
        "Date": "Fri, 26 Aug 2016 22:27:32 GMT",
        "Transfer-Encoding": "chunked",
        "Connection": "close",
        "Server": "Apache",
        "Content-Security-Policy": "referrer no-referrer;"
    },
    "Status": {
        "200": "OK"
    }
}
</code></pre>
<p>This is an example of runnng /get_ip?uri=www.example.com for Google.</p>
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
<p>This is an example of running /bitcoin?address=<wallet address> for 1ArJ9vRaQcoQ29mTWZH768AmRwzb6Zif1z</p>
<pre><code>{
    "address": "1ArJ9vRaQcoQ29mTWZH768AmRwzb6Zif1z",
    "balance": 0,
    "final_balance": 0,
    "final_n_tx": 4,
    "n_tx": 4,
    "total_received": 82530000,
    "total_sent": 82530000,
    "txrefs": [
        {
            "spent": false,
            "tx_hash": "474cce51a9c4b265d4da0257acb21a554563fd41200970996e2b8914dc6f1d68",
            "tx_output_n": -1,
            "confirmations": 129941,
            "confirmed": "2014-04-23T11:44:27Z",
            "value": 11550000,
            "tx_input_n": 0,
            "block_height": 297305,
            "ref_balance": 0,
            "double_spend": false
        }
    ],
    "unconfirmed_balance": 0,
    "unconfirmed_n_tx": 0
}
</code></pre>
