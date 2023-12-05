from django.http import HttpResponse, HttpRequest

def allowed_methods(allowed_methods: str):
    allowed_methods_list = allowed_methods.split(',')

    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.method not in allowed_methods_list:
                return HttpResponse('Method Not Allowed', status=405)
            return func(request, *args, **kwargs)
        return wrapper

    return decorator
