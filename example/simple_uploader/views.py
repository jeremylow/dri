from django.views.generic import CreateView, DetailView

from simple_uploader.models import ImageModel


class SimpleImageUploaderView(CreateView):
    model = ImageModel
    template_name = 'simple_uploader/index.jinja'
    fields = ['image']


class ImageDetailView(DetailView):
    model = ImageModel
    template_name = 'simple_uploader/detail.jinja'
