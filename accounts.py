from parsing import get_cookies

def get_accounts():
    accounts = []
    afile = open("accounts.txt", "r")
    alines = afile.readlines()
    for a in alines:
        acs = a.strip().split(":")
        acc = Account(acs[0],acs[1])
        cookies = get_cookies(a)
        if cookies != None:
            acc.cookies = cookies
        accounts.append(acc)
    return accounts

class Account:
    def __init__(self,login,password):
        self.login=login
        self.password=password
        self.cookies=None
        self.token=None
        self.birthday=None
        self.email=None
        pass

    def __str__(self):
        attrs=["login","password","email","birthday","token","cookies"]
        str=""
        for attr in attrs:
            attr_value=getattr(self,attr)
            if attr_value!=None:
                str+=f"{attr_value}:"
        return str.rstrip(':')+"\n"

    def add_info(self,info):
        if "email" in info:
            self.email=info["email"]
        if "birthday" in info:
            self.birthday=info["birthday"]
        pass


