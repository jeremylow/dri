from django.conf import settings

RESP_IMG_BREAKPOINTS = getattr(
	settings,
	"RESP_IMG_BREAKPOINTS",
	[320, 453, 579, 687, 786, 885, 975, 990])

RESP_IMG_QUALITY = getattr(settings, "RESP_IMG_QUALITY", 80)
RESP_IMG_THREAD = getattr(settings, "RESP_IMG_THREAD", True)
RESP_IMG_FILETYPES = getattr(
	settings,
	"RESP_IMG_FILETYPES",
	['jpg', 'jpeg', 'jpe', 'png', 'webp'])