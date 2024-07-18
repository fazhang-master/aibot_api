from django.urls import include,path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/',include('VDP.urls'))
]
