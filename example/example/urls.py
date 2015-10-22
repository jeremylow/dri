from django.conf import settings
from django.conf.urls import url, patterns


from simple_uploader.views import SimpleImageUploaderView, ImageDetailView

urlpatterns = patterns(
    '',
    url(r'^$', SimpleImageUploaderView.as_view(), name="uploader"),
    url(r'^(?P<pk>[0-9]+)/$', ImageDetailView.as_view(), name="viewer")

)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
