



# configures user detection

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'farmDashboard'
        return redirectUrl

 
    elif user.role == 2:
         redirectUrl = 'customerDashboard'
         return redirectUrl
    
    # a super User can log in and get diected to admin panel
    
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl