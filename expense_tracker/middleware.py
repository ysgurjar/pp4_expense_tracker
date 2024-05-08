from django.http import Http404

class BlockAuthURLsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_paths = [
            '/password_change/',
            '/password_change/done/',
            '/password_reset/',
            '/password_reset/done/',
            '/reset/<uidb64>/<token>/',
            '/reset/done/',
        ]

    def __call__(self, request):
        if request.path in self.blocked_paths:
            raise Http404("This page is not available.")
        return self.get_response(request)