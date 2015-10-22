from django.db import models
from django.core.urlresolvers import reverse


from django_dri.fields import ResponsiveImageField


class ImageModel(models.Model):

    """ Class to provide storage of an image """

    image = ResponsiveImageField(upload_to='images')

    def get_absolute_url(self):
        return reverse('viewer', kwargs={'pk': self.id})
