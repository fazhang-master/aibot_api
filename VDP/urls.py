from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from .views.background_video import SystemBackgroundVideo, CustomBackgroundVideo
from .views.background_stickers import SystemBackgroundSticker, CustomBackgroundSticker
from .views.background_picture import SystemBackgroundPicture, CustomBackgroundPicture
from .views.upload_tmpfile import TemporaryFileUpload
from .views.remove_videogreenscreen import RemoveVideoGreenScreen
from .views.crawle_file import CrawerFile
from rest_framework.routers import DefaultRouter
from .views.RegisterandLogin import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('SystemBackgroundVideo/', SystemBackgroundVideo.as_view({'get':'list'})),
    path('CustomBackgroundVideo/', CustomBackgroundVideo.as_view({'post':'upload','get':'list','delete':'delete_video'})),

    path('SystemBackgroundSticker/', SystemBackgroundSticker.as_view({'get':'list'})),
    path('CustomBackgroundSticker/', CustomBackgroundSticker.as_view({'post':'upload','get':'list','delete':'delete_video'})),

    path('SystemBackgroundPicture/', SystemBackgroundPicture.as_view({'get':'list'})),
    path('CustomBackgroundPicture/', CustomBackgroundPicture.as_view({'post':'upload','get':'list','delete':'delete_video'})),

    path('TemporaryFileUpload/', TemporaryFileUpload.as_view({'post':'create'})),

    path('RemoveVideoGreenScreen/', RemoveVideoGreenScreen.as_view({'get':'retrieve'})),

    path('CrawerFile/', CrawerFile.as_view({'post':'upload','get':'list','delete':'delete_video'})),

    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 生产环境中，通常你会通过Web服务器如Nginx来服务媒体文件，这里仅为示例
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]