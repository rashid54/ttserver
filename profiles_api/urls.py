from django.urls import path,include
from rest_framework.routers import DefaultRouter

from profiles_api import views

router= DefaultRouter()
router.register('profile',views.UserProfileViewSet)
router.register('question',views.QuestionItemViewSet)
router.register('test',views.TestViewSet)
router.register('getid',views.GetUser,base_name = "getid")
router.register('gettestquestion/(?P<pk>.+)',views.GetTestQuestion,base_name= "get_ques")
router.register('testresult',views.TestResultViewSet)
router.register('selectedans',views.SelectedAnsViewSet)

urlpatterns = [
    path('login/',views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]
