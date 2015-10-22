import os
import tempfile
import subprocess
import shlex

from queue import Queue
from threading import Thread

from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.text import slugify
from django.core.files.storage import default_storage

import multiprocessing


CPU_COUNT = multiprocessing.cpu_count()

RESP_IMG_BREAKPOINTS = [320, 453, 579, 687, 786, 885, 975, 990]
RESP_IMG_QUALITY = 80
RESP_IMG_THREAD = True
RESP_IMG_FILETYPES = ['jpg', 'jpeg', 'jpe', 'png', 'webp']

conversion_queue = Queue()


def image_converter_worker(q):
    while True:
        cmd = q.get()
        print('got', cmd)
        subprocess.check_call(shlex.split(cmd))
        print('finished with file')
        q.task_done()


for i in range(CPU_COUNT * 4):
    worker = Thread(target=image_converter_worker, args=(conversion_queue,))
    worker.setDaemon(True)
    worker.start()


class ResponsiveImageField(models.FileField):

    def __init__(self, *args, **kwargs):
        """
        Args:
            breakpoints (list[int]): List of image widths to which original
                image should be converted. Default is:
                [320, 453, 579, 687, 786, 885, 975, 990]
            quality (int): ImageMagick quality setting. Note that this is
                considerably different than what you might expect when
                exporting from Photoshop or the like. Default is 80,
                which is equivalent to something like Photoshop 60.
            threading (bool): Use the python threading module to run the
                image conversion. This process is asynchronous, so if you click
                through to save the model (from something like a CreateView),
                the conversion will run in the background, meaning that all of
                the 'sources' images may not yet be available.
                Defaults to True.

        TODO: Add kwargs for celery tasks.

        """

        self.breakpoints = getattr(settings,
                                   'RESP_IMG_BREAKPOINTS',
                                   RESP_IMG_BREAKPOINTS)

        self.quality = getattr(settings, 'RESP_IMG_QUALITY', RESP_IMG_QUALITY)
        self.threading = getattr(settings, 'RESP_IMG_THREAD', RESP_IMG_THREAD)
        self.filetypes = getattr(settings,
                                 'RESP_IMG_FILETYPES',
                                 RESP_IMG_FILETYPES)

        self.convert_cmd = (
            'convert {input_name}  -thumbnail {size}  -quality {qual}'
            ' -unsharp 0.05x0.05+12+0.001'
            ' -filter Triangle'
            ' -define filter:support=4'
            ' -define jpeg:fancy-upsampling=off'
            ' -define png:compression-filter=5'
            ' -define png:compression-level=9'
            ' -define png:compression-strategy=1'
            ' -define png:exclude-chunk=all'
            ' -interlace Line'
            ' -modulate 115,110,100'
            ' {output_name}-{size}{ext}'
        )
        super(ResponsiveImageField, self).__init__(*args, **kwargs)

    def _get_avaible_name(self, image):
        """ Return an available file name for the saved image.

        Args:
            image: name of the image to be saved.

        Returns:
            Slugify'd available name.

        """

        print(getattr(settings, 'MEDIA_ROOT'))
        upload_path = os.path.join(
            getattr(settings, 'MEDIA_ROOT'),
            self.upload_to)
        print(upload_path)

        upload_name = slugify(os.path.basename(image))

        return default_storage.get_available_name(
            os.path.join(upload_path, upload_name))

    def clean(self, *args, **kwargs):
        """
        So we need to convert it to a File object, so that we can get the
        save method on it and return an unused filename, right?
        """

        data = super(ResponsiveImageField, self).clean(*args, **kwargs)

        output_name = self._get_avaible_name(data.name)
        ext = os.path.splitext(data.name)[1]

        if type(data.file) == InMemoryUploadedFile:
            input_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
            [input_file.write(chunk) for chunk in data.file.chunks()]
            input_file.seek(0)

        elif type(data.file) == File:
            input_file = data.file

        try:
            save_dir = os.path.dirname(
                os.path.join(
                    settings.MEDIA_ROOT,
                    self.upload_to))

            for breakpoint in self.breakpoints:
                cmd = self.convert_cmd.format(
                    input_name=input_file.name,
                    qual=self.quality,
                    output_dir=save_dir,
                    output_name=output_name,
                    size=breakpoint,
                    ext=ext)
                conversion_queue.put(cmd)

            data.name = output_name + ext

        except KeyError as e:
            print('Image field ({0}) not found'.format(e))

        return data
