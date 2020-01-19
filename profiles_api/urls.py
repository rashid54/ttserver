from django.urls import path,include
from rest_framework.routers import DefaultRouter

from profiles_api import views

router= DefaultRouter()
router.register('profile',views.UserProfileViewSet)
router.register('question',views.QuestionItemViewSet)
router.register('test',views.TestViewSet)

urlpatterns = [
    path('login/',views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]