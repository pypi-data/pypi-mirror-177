# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['head_context']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'head-context',
    'version': '0.1.0',
    'description': '',
    'long_description': '# `head-context`\n\nEasily manage your assets in meta tags (scripts, css, preload etc.) from anywhere\nin the template code (and outside).\n\n## Why\n\nImagine a form widget, which requires a heavy image processing library that we want to include ONLY IF the widget itself was rendered. Thanks to `head-context` you can specify what resources you need locally (in template fragments, widgets and so on) yet load them in the `head` section of your page with ease.\n\n## What does it do?\n\n```html+jinja\n<!doctype html>\n<html>\n<head>\n    <title>My Title!</title>\n    <!-- this is where we want all our js/css rendered to be rendered -->\n    {{ meta_placeholder() }}\n</head>\n<body>\n    {% include "my-cool-component.html" %}\n</body>\n</html>\n```\n\nAnd `my-cool-component.html`:\n\n```html+jinja\n<!-- we can call these from anywhere and they will be automatically rendered in the right place! -->\n{% do push_js(\'/static/cool-component.js\', mode="async") %}\n{% do push_css(\'/static/cool-component.css\') %}\n{% do push_preload(\'/static/some-image-we-need.png\', \'image\') %}\n<div class="my-cool-component">\n    <!-- ... --->\n</div>\n```\n\nAnd that\'s pretty much it. You can `push_js`/`push_css`/`push_preload` from anywhere in the template (and even outside of templates) and it will be automatically attached to the page being rendered.\n\n## Features\n\n* Supports scripts, styles and preload directives\n* Works with Jinja2\n* Can be used outside of templates too\n  * if you want to render a custom (form) widget for example\n',
    'author': 'Rafal Stozek',
    'author_email': 'rafal.stozek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafales/head-context',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
