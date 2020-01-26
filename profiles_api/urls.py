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
router.register('resetpassword',views.ResetPassword,base_name="rest")

urlpatterns = [
    path('login/',views.UserLoginApiView.as_view()),
    path('',include(router.urls)),
    path('confirm/<slug:uid>/',views.send_confirm_email,name='confirm_email'),
    path('activate/<slug:uidb64>/<slug:token>/',views.activate_account, name='activate'),
    path('resetpass/',views.reset_password_email,name='reset_password_email'),
    path('reset/<slug:uidb64>/<slug:token>/',views.reset_password, name='reset_password'),

]
