from django.http import JsonResponse


def not_authorized():
    return JsonResponse({'status': 'error','message': 'Not Authorized'}, status=403)


def not_found():
    return JsonResponse({'status': 'error','message': 'Not Found'}, status=404)


def error():
    return JsonResponse({'status': 'error','message': 'Internal Server Error'}, status=500)


def bad_request(error_message):
    return JsonResponse({'message': 'Bad request', 'message': error_message}, status=400)


def success(status, success_message, data={}):
    return JsonResponse({'status': status,
                         'result': data,
                         'message': success_message}, status=200)
