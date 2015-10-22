#WORK IN PROGRESS

#WILL BREAK AND/OR DESTROY EVERYTHING YOU HOLD DEAR



Not really a readme yet, just a collection of notes.

### Settings variables:

You don't need to set any of these, the defaults should work for most use cases.

* RESP_IMG_BREAKPOINTS [Optional]

    Type: List

    Default: ``[320, 453, 579, 687, 786, 885, 975, 990]``

    Description: List of integers. Each integer represents the width of the output image. E.g., [100, 200] and each of your images will be resized to 100px wide and 200px wide.

* RESP_IMG_QUALITY [Optional]

    Type: Integer

    Default: ``80``

    Description: Image's output quality. Note that this is ImageMagick's setting not a Photoshop setting.

* RESP_IMG_THREAD [Optional]

    Type: Bool

    Default: ``True``

    Description: Whether to use python threads to convert the images. Highly recommended.

* RESP_IMG_UPLOAD_PATH [Optional]

    Type: String

    Default: ``''``

    Description: If provided, upload the images to the given folder **under** your MEDIA_ROOT folder. Otherwise, they just get saved in your MEDIA_ROOT folder.

* RESP_IMG_FILETYPES [Optional]

    Type: List

    Default: ``['jpg', 'jpeg', 'jpe', 'png', 'webp']``

    Description: Image types subject to conversion. Should be a list of strings so, for example, ['jpg', 'jpeg', 'png', 'webp']. Uses the image's extension. The image is then checked against the backend.