from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()


# router.register('titles', TitleViewSet, basename='titles')
# router.register('categories', CategoryViewSet, basename='category')
# router.register('genres', GenreViewSet, basename='genres')
# router.register('users', UserViewSet, basename='users')


# urls_auth = [
#     path('token/', get_token, name='get_token'),
#     path('email/', create_new_user, name='email')
# ]

# urlpatterns = [
#     path('v1/', include(router.urls)),
#     path('v1/auth/', include(urls_auth))
# ]
