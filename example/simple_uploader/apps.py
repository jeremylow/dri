from django.apps import AppConfig


class SimpleUploaderConfig(AppConfig):
    name = 'simple_uploader'

    def ready(self):
        import simple_uploader
