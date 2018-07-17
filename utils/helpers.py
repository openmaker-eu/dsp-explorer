def get_host(request):
    if request.is_secure():
        protocol = 'https://'
    else:
        protocol = 'http://'
    return protocol + request.get_host()
