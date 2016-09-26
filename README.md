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

Quick Buy Links:

    $ 21 buy https://www.request402.com/ip --> Get the origin of your IP address.
    $ 21 buy https://www.request402.com/get --> Return GET data.
    $ 21 buy https://www.request402.com/server-location --> Return header and server location data.
    $ 21 buy https://www.request402.com/domain_status --> Get the header, status, and trustworthiness of a specfic domain url.
    $ 21 buy https://www.request402.com/domain_ip --> Get the origin IP address of a specific domain url.
    $ 21 buy https://www.request402.com/ssl-cert --> Return public key of SSL certificate for verification.
    $ 21 buy https://www.request402.com/company-contact --> Return public key of SSL certificate for verification.
    $ 21 buy https://www.request402.com/twitter --> Return demographic and social media account information of a Twitter username.
    $ 21 buy https://www.request402.com/bitcoin?address=<wallet address> --> Wallet Address Information


<b>PURCHASE:</b> $ 21 buy https://www.request402.com/ip

<pre><code>{
    "origin": xxx.xxx.x.xx
}
</code></pre>
