```                
                Get Facebook Cookies and Access Token v1.4.0  
    _            __     __  _ _             __          __  _     
   | |           \ \   / / | | |            \ \        / / | |    
   | |__  _   _   \ \_/ /__| | | _____      _\ \  /\  / /__| |__  
   | '_ \| | | |   \   / _ \ | |/ _ \ \ /\ / /\ \/  \/ / _ \ '_ \ 
   | |_) | |_| |    | |  __/ | | (_) \ V  V /  \  /\  /  __/ |_) |
   |_.__/ \__, |    |_|\___|_|_|\___/ \_/\_/    \/  \/ \___|_.__/ 
           __/ |                                                  
          |___/             https://yellowweb.top                 

If you like this script, PLEASE DONATE!  
USDT TRC20: TKeNEVndhPSKXuYmpEwF4fVtWUvfCnWmra
Bitcoin: bc1qqv99jasckntqnk0pkjnrjtpwu0yurm0qd0gnqv  
Ethereum: 0xBC118D3FDE78eE393A154C29A4545c575506ad6B  
```

# Description
This script logs in to Facebook using login and password, gets access token and cookies and writes it all into a text file. 
It can optionally get account's birthday and email using Tinder app, that it adds to the account.

# !Warning!
Be aware that if your accounts were registered using a proxy from one country (for example UA) and now you use for this script a proxy from some
other country (like RU), then there is a big chance that Facebook won't login your account. You'll get a "Wrong username or password" error in my script then.
To check, if this is the case, create a profile in your antidetect browser with your proxy and try to login. If you can't - then change your proxies so they match
account's country and try again in the browser. Only after you are able to login in the browser - start the script.

# Usage
0. Install the latest version of Python. Don't use 2.x, only 3.10 or later. Then install all the requirements from `requirements.txt` using:<br>
`pip install -r requirements.txt`
1. Create an `accounts.txt` file, put your logins and passwords delimited by semicolon like:<br>
`login1:pass1`<br>
`login2:pass2`<br>
and so on...<br>
If you want, you can use accounts with cookies, then the login part will be skipped. Accounts with cookies should look like this:<br>
`login:pass:[cookies in json format]`
2. Create a `proxy.txt` file and put your HTTP proxy (or several HTTP proxies line by line) like this:<br>
`ip:port:login:password(ipupdatelink)`<br>
If you don't need ip update link then just use: `ip:port:login:password`<br>
If you add multiple proxies they will be used in a round robbin manner.<br>
**This script doesn't (and won't) support SOCKS proxies.**
3. Run the script using: `python3 main.py`
4. If you don't need birthday and email then answer 'N' to the question about adding Tinder app
5. After everything is done all the account's info will be saved to `parsed.txt` file.

*Happy hacking!*
