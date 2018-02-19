from django.http import JsonResponse


def graphql_error_response(message, status_code=400):
    error = {'message': message}
    return JsonResponse({'errors': [error]}, status=status_code)
