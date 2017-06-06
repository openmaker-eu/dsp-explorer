from django.http import JsonResponse


def not_authorized():
    return JsonResponse({'error': 'Not Authorized'}, status=403)


def not_found():
    return JsonResponse({'error': 'Not Found'}, status=404)


def error():
    return JsonResponse({'error': 'Internal Server Error'}, status=500)

def bad_request(error_message):
    return JsonResponse({'error': 'Bad request', 'message':error_message}, status=400)

def success(success_message, data):
    return JsonResponse({'status': 'ok',
                         'result': data,
                         'message': success_message}, status=200)
