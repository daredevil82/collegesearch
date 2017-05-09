import logging

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from collegesearch.settings import REST_FRAMEWORK


class BaseView(APIView):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('django')
