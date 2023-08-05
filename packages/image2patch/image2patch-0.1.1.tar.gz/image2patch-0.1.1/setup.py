# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['image2patch']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1,<2']

setup_kwargs = {
    'name': 'image2patch',
    'version': '0.1.1',
    'description': 'A library that splits the image into overlapping or non-overlapping patches with the optimal step in order to minimize pixels loss. It can then merge them back together.',
    'long_description': '# image2patch\n`image2patch` splits the image in different patches with automatic detection of the best step in order to minimize pixels loss. The overlap between patches depends on the patch size.\nAlternatively, it is possible to choose the step size.  \nThe reconstruction of the original image is possible using `patch2image` which can merge the patches taking into account the overlap percentage among patches. Hence, the original image is perfectly restored. \nIf there is a minimum pixels loss during patching procedure, resize to its original dimensions is possible. \n\n## Example\n![pic](example.png)\n\n## Installation\n```Python\npip install image2patch\n```\n```Python\nfrom image2patch import image2patch\n```\n```Python\nfrom image2patch import patch2image\n```\n## How to use it\n`image2patch(image, patch_size, step=None, verbose=False)`\n\nIn particular:\n- image : 2D input image\n- patch_size : dimension of the window\n- step : the distance from one step to another, if =None it will be automatically detected in order to avoid pixels loss. If set = patch_size it will provide patches without overlapping but with pixels loss depending on the size of the input image. \n- verbose : if =True it provides details. \n \n\n`patch2image(patched_image, original_dims, step, resize_flag = True)`\n\nIn particular:\n- patched_image : 2D input patches from image2patch\n- original_dims : dimension of the original image\n- step : step obtained from `image2patch`\n- resize_flag : allows to resize the image to its original dimension in case of pixels loss. \n\n \n## Licence\n[MIT](https://choosealicense.com/licenses/mit/)\n\n',
    'author': 'Luca Pavirani',
    'author_email': 'luca481998@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LucaPavirani/image2patch.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
