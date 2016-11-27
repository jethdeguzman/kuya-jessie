from django.conf.urls import url
from .views import Callback

urlpatterns = [
    url(r'messenger/', Callback.as_view()),
]
