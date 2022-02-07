# Description
This script logs in to Facebook using login and password, gets access token and cookies and writes it all into a text file. 
It can optionally get account's birthday and email using Tinder app, that it adds to the account.

# Usage
0. Install all the requirements from `requirements.txt` using:<br>
`pip install -r requirements.txt`
1. Create an `accounts.txt` file, put your logins and passwords delimited by semicolon like:<br>
`login1:pass1`<br>
`login2:pass2`<br>
and so on...<br>
If you want, you can use accounts with cookies, then the login part will be skipped. Accounts with cookies should look like this:<br>
`login:pass:[cookies in json format]`
2. Create a `proxy.txt` file and put your proxy (or several proxies line by line) like this:<br>
`ip:port:login:password:ipupdatelink`<br>
If you don't need ip update link then just use: `ip:port:login:password`<br>
If you add multiple proxies they will be used in a round robbin manner.
3. Run the script using Pyton 3.7 or higher: `python3 YWB.FBLogin.py`
4. If you don't need birthday and email then answer 'N' to the question about adding Tinder app
5. After everything is done all the account's info will be saved to `parsed.txt` file.

*Happy hacking!*
