def detectUser(user):
    if user.role == 1:
        redirectUrl = 'clinicDashboard'
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
    return redirectUrl