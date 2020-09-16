from django.urls import path, include
from . custom_router import NoRootRouter
from . import api_views

router = NoRootRouter()
router.register('chitty', api_views.ChittyViewSet, 'chitty')
router.register('members', api_views.MemberViewSet, 'member')
router.register('logs', api_views.LogViewSet, 'log')

app_name = 'onam_chitty'

urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace = 'api')),
]