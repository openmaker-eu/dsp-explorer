from ..site_helpers import User

def authorization(request):
    '''
    Define user page level authorization(@TODO: EX badge system)
    :param request:
    :return: authorization dictionary
    '''
    return {'om_authorization': User.authorization(request)}
