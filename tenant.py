import requests
import pxpshell

class Tenant:
    
    def __init__(self,name,client_secret,client_id,tenant_id):
        self.token = ""
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.user_list = []
        self.name = name
        self.curr_user = ""
        
    
    def delegation(self):
      
        
        x = pxpshell.pxpowershell()
        x.start_process()
        result = x.run("Connect-ExchangeOnline -CertificateThumbPrint '' -AppID '' -Organization ''")
        print(result.decode())
        x.stop_process()
        

    def get_user_list(self):
        count = 0
        url = "https://graph.microsoft.com/v1.0/users"
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.get(url, headers = headers)
        data = response.json()
        UPNs = []

        for item in data['value']:
            UPNs.append([data['value'][count]['userPrincipalName'],data['value'][count]['id']] )
            count += 1
        
        if response.status_code == 200:
            print("UPNs - 200")
            return UPNs
        else:
            return none

    def reset_pw(self):

         force_change = input("Force change at next sign in?:")
         password = input("Password: ")
         data = {
                    "passwordProfile":{
                        "forceChangePasswordNextSignIn": force_change,
                        "password": password
                        }
                }
         
         auth = {"Authorization": 'Bearer ' + self.token,
                 "Content-Type": "application/json"}
         url = "https://graph.microsoft.com/v1.0/users/" + self.curr_user
         try:
             response = requests.patch(url, json=data, headers = auth)
         except:
             print("Error reseting password")

    def check_token(self):
        print("Checking if " + self.token + " Is valid")
        auth = {"Authorization": 'Bearer ' + self.token,
                 "Content-Type": "application/json"}
        url = "https://graph.microsoft.com/v1.0"

        try:
             response = requests.get(url, headers = auth)
        except:
             print("error validating auth token")

     
    def get_token(self):

        print("Getting token for " + self.name)
        
        obj = {  
               "grant_type": "client_credentials",
               "client_secret": self.client_secret, 
               "client_id": self.client_id,
               "scope": "https://graph.microsoft.com/.default"
               }
        url = 'https://login.microsoftonline.com/{' + self.tenant_id + '}/oauth2/v2.0/token'
        x = requests.post(url, obj)
        response = x.json()
        self.token = response["access_token"]
        


    def update_usr(self):
        try:
            self.check_token()
            first_name = input("Please enter your first name: ")
            while not first_name.isalpha():
                print("Invalid input! First name must contain only letters.")
                first_name = input("Please enter your first name: ")
            last_name = input("Please enter your last name: ")
            while not last_name.isalpha():
                print("Invalid input! Last name must contain only letters.")
                last_name = input("Please enter your last name: ")
            display_name = first_name + " " + last_name

            data   ={
                  "displayName": display_name,
                  "givenName": first_name,
                  "surname": last_name
                    }
      
            headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
            print(self.curr_user[1])
            url = f"https://graph.microsoft.com/v1.0/users/{self.curr_user[0]}"
            response = requests.patch(url, json = data, headers=headers)
            response.raise_for_status()
            print("User information updated successfully!")
        except Exception as e:
            print("Error occured when updating name", e)
                

    def print_tenant(self):
        print(self.name + " " + self.client_secret + " " + self.client_id + " " + self.tenant_id)

    def select_user(self):
        if len(self.token) < 2:
            self.get_token()

        if len(self.user_list) < 5:
            print("d")
            self.user_list = self.get_user_list()
        
        count = 0
        UPN = []
        choice = input("Username: ")
        if choice == "0":
            return 2
        print(self.user_list)
        for user in self.user_list:
            
            if choice.lower() in user[0].lower():
                UPN = user
                print("Found match")
                count += 1


        if count == 1:
            self.curr_user = UPN 
            print("Selected " + UPN[0])
        elif count > 1:
            print("Found more than 1 match, try again")
            return 1
        elif count != 1:
            print("No matches found")
            return 1
            

    def __del__(self):
        return 0
