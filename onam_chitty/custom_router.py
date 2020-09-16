from rest_framework.routers import DefaultRouter

class NoRootRouter(DefaultRouter):
    include_root_view = False
