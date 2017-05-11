from eve import Eve
from eve.auth import BasicAuth

class Authenticate(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource,
                   method):
        print resource
        print method
        if  method == 'GET':
            user = app.data.driver.db['users']
            user = user.find_one({'username': username,'password':password})

            if user:
                return True
            else:
                return False
        elif resource == 'users' and method == 'POST':
            print username
            print password
            return username == 'mk' and password == 'balibartapipswd'
        else:
            return True

app = Eve(settings='settings.py', auth=Authenticate)
app.run()
