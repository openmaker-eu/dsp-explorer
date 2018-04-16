

def authorization(request):
    '''
    Define user page level authorization(@TODO: EX badge system)
    :param request:
    :return: authorization dictionary
    '''
    om_authorization = \
        30 if False else \
        20 if False else \
        10 if request.user.is_authenticated() \
        else 0

    return {'om_authorization': om_authorization}
