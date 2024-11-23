class SessionManagementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_session = request.session.get('user_session_id')
        if not user_session:
            request.session['user_session_id'] = 'new_session_value'
        response = self.get_response(request)
        return response
