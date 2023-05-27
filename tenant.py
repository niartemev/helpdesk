import requests
import pxpshell

class Tenant:
    
    #initializes the tenant object with the name, client secret, client id, and tenant id
    def __init__(self,name,client_secret,client_id,tenant_id, app_id, thumb_print):
        self.token = ""
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.client_secret = client_secret
        self.name = name
        self.appid = app_id
        self.thumb_print = thumb_print
        self.user_list = []
        self.curr_user = ""
        self.UPNs = []
       

        #self.get_token()       
        #self.get_user_list()
    
    
    def change_MFA(self):
        print("change mfa")

        auth = {"Authorization": 'Bearer ' + self.token,
                 "Content-Type": "application/json"}
        url = ""
        body = {
                "phoneNumber": "+",
                "phoneType": "mobile",
                }
        try:
            response = requests.patch(url, json = body, headers = auth)
            #x = response.json()
            print(str(response))
        except:
            print("error validating auth token")

    #delegate email access via exov2 module  
    def delegate_em(self, manage, sendas, sendonbehalf, forwarding, fromUser, toUser, remove ):
      

       cmd = f"Connect-ExchangeOnline -CertificateThumbPrint '{self.thumb_print}' -AppID '{self.appid}' -Organization '{self.name}'"
       
       if remove == True:
           if manage == True:
               cmd += "; Remove-MailboxPermission -Identity " + fromUser + " -User " + toUser + " -AccessRights FullAccess" + " -Confirm:$false"
           if sendas == True:
               cmd += "; Remove-RecipientPermission " + fromUser + " -Trustee " + toUser + " -AccessRights SendAs"+ " -Confirm:$false"
           if sendonbehalf == True:
               cmd += "; Set-Mailbox -Identity " + fromUser + " -GrantSendOnBehalfTo $null"+ " -Confirm:$false"
           if forwarding == True:
               cmd += "; Set-Mailbox -Identity "+ fromUser + " -ForwardingAddress $null" + " -Confirm:$false"
       else:
           if manage == True:
               cmd += "; Add-MailboxPermission -Identity " + fromUser + " -User " + toUser + " -AccessRights FullAccess" + " -Confirm:$false"
           if sendas == True:
                cmd += "; Add-RecipientPermission " + fromUser + " -Trustee " + toUser + " -AccessRights SendAs"+ " -Confirm:$false"
           if sendonbehalf == True:
               cmd += "; Set-Mailbox -Identity " + fromUser + " -GrantSendOnBehalfTo " + toUser+ " -Confirm:$false"
           if forwarding == True:
               cmd += "; Set-Mailbox -Identity "+ fromUser + " -ForwardingAddress "+ toUser + " -Confirm:$false"

       x = pxpshell.pxpowershell()
       x.start_process()
       result = x.run(cmd)
       print(result.decode())
        
       x.stop_process()
    
    #delegate calendar permissions
    def delegate_cal(self, fromUser, toUser, remove):
        
        
        
        cmd = f"Connect-ExchangeOnline -CertificateThumbPrint '{self.thumb_print}' -AppID '{self.appid}' -Organization '{self.name}'"
        if remove == True:
            cmd += "; Remove-MailboxFolderPermission -Identity " + fromUser + ":\Calendar -User " + toUser + " -Confirm:$false"
        else:
            cmd += "; Add-MailboxFolderPermission -Identity " + fromUser + ":\Calendar -User " + toUser + " -AccessRights Editor -Confirm:$false"
        x = pxpshell.pxpowershell()
        x.start_process()
        result = x.run(cmd)
        print(result.decode())
        x.stop_process()


    #get a list of users in the tenant
    def get_user_list(self):
        count = 0
        url = "https://graph.microsoft.com/v1.0/users"
        headers = {'Authorization': 'Bearer ' + self.token}
        response = requests.get(url, headers = headers)
        data = response.json()
        UPNs = []
        
        if response.status_code == 200:
            for item in data['value']:
                UPNs.append([data['value'][count]['userPrincipalName'],data['value'][count]['id']] )
                count += 1
            print("UPNs - 200")
            self.UPNs = UPNs
            return UPNs
        else:
            return 0

    #reset the password of a user
    def reset_pw(self, value, force_ch, window, pw):
        
        if(self.check_token()):
            print("Token invalid")
            return 0
        else:
            window.statusWindow.append("Resetting password for " + str(value) + " " + pw)

            data = {
                    "passwordProfile":{
                        "forceChangePasswordNextSignIn": force_ch,
                        "password": pw
                        }
                    }
            auth = {"Authorization": 'Bearer ' + self.token,
                    "Content-Type": "application/json"}

            url = "https://graph.microsoft.com/v1.0/users/" + value

            try:
                response = requests.patch(url, json=data, headers = auth)
            except Exception as e:
                window.statusWindow.append(e)
        
            if str(response.status_code) == "204":
                window.statusWindow.append("Password for " + str(value) + " successfully reset;force change: " + str(force_ch))
                return 1
            else:
                window.statusWindow.append("Error resetting password for " + value)
                return 0

 

    #check if the api token is valid
    def check_token(self):
        

        #print("Checking if " + self.token + " Is valid")
        auth = {"Authorization": 'Bearer ' + self.token,
                 "Content-Type": "application/json"}
        url = "https://graph.microsoft.com/v1.0/organization"

        try:
             response = requests.get(url, headers = auth)
             x = response.json()
             print(x["value"][0]["verifiedDomains"][0])#[0]["name"])
        except:
             print("error validating auth token")

    #get graph api token 
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
        
        

    #update the display name of a user
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

    def return_self(self):
        return (self.name)# + " " + self.client_secret + " " + self.client_id + " " + self.tenant_id) 

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
