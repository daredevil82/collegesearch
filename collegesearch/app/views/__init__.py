import logging
import os


from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

from rest_framework.views import APIView


class BaseView(APIView):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('django')


class IndexView(View):
    """
    Serves the compiled react build files, resulting from npm run build.  If files don't exist, return a 501
    """
    def get(self, request):
        try:
            with open(os.path.join(settings.REACT_APP_DIR, 'build', 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse('This URL is valid only if you have the production version of the app.  Use [{}] '
                                'instead, or execute npm run build to rebuild the production '
                                'version'.format(settings.ALLOWED_HOSTS[0]), status = 501)
