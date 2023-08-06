# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cumo',
 'cumo._internal',
 'cumo._internal.members',
 'cumo._internal.protobuf',
 'cumo._vendor.pypcd']

package_data = \
{'': ['*'], 'cumo': ['public/*']}

install_requires = \
['Pillow>=9,<10',
 'numpy>=1,<2',
 'protobuf>=3,<4',
 'python-lzf>=0.2.4,<0.3.0',
 'websockets>=8,<9']

setup_kwargs = {
    'name': 'cumo',
    'version': '0.25.0',
    'description': 'Webブラウザ上に点群を描画する python ライブラリ',
    'long_description': '# cumo\n\n## ビルド\n\nyarn、protoc、poetryが必要です（`.devcontainer/Dockerfile`参照）。\n以下のようにすると`lib/dist`にtar.gzとwhlファイルが生成されます。\nクライアントのHTML等はライブラリに埋め込まれています。\n\n```console\n$ ./build.sh\n```\n\n## インストール\n\n```console\n$ pip install pointcloud-viewer\n```\n\n## ドキュメント\n\nsphinxでドキュメントの生成が可能です。\n\n```console\n$ cd lib\n$ poetry install\n$ poetry run sphinx-apidoc --append-syspath -F -o ./docs .\n```\n\n## 使用例\n\n`lib/cumo/__main__.py`は3面図を撮る例です。\n\n```console\n$ poetry run python -m cumo pcl_logo.pcd\nopen: http://127.0.0.1:8082\nsetup...\nresize window and press custom control button "start"\nsaved: screenshot_x.png\nsaved: screenshot_y.png\nsaved: screenshot_z.png\n```\n\nREPLでの使用も可能です。\n\n```console\n$ poetry run python\nPython 3.8.7 (default, Apr  9 2022, 21:34:33)\n[GCC 9.4.0] on linux\nType "help", "copyright", "credits" or "license" for more information.\n>>> from cumo import PointCloudViewer\n>>> viewer = PointCloudViewer()\n>>> viewer.start()\n>>> # open localhost:8082 on your browser\n>>> with open(filename, "rb") as f:\n>>>     b = f.read()\n>>>     viewer.send_pointcloud_pcd(b)\n```\n',
    'author': 'Kurusugawa Computer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kurusugawa-computer/cumo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
