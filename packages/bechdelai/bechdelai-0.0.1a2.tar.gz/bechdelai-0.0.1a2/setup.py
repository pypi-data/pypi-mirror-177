# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bechdelai',
 'bechdelai.audio',
 'bechdelai.data',
 'bechdelai.data.src',
 'bechdelai.data.tests',
 'bechdelai.image',
 'bechdelai.scripts',
 'bechdelai.text',
 'bechdelai.utils',
 'bechdelai.video',
 'bechdelai.video.old']

package_data = \
{'': ['*']}

install_requires = \
['Click>=8.0.4',
 'PyMuPDF>=1.19.6,<2.0.0',
 'beautifulsoup4>=4.10.0',
 'chardet>=4.0.0',
 'deepface>=0.0.68,<0.0.69',
 'ftfy>=6.1.1,<7.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'lxml>=4.8.0,<5.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'mediapipe>=0.9.0,<0.10.0',
 'numpy>=1.21.3,<2.0.0',
 'opencv-python>=4.5.4,<5.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'plotly>=5.3.1,<6.0.0',
 'python-dotenv>=0.19.2',
 'pytube>=12.1.0,<13.0.0',
 'requests>=2.26.0',
 'retina-face>=0.0.12,<0.0.13',
 'scikit-learn>=1.0.1,<2.0.0',
 'tensorflow>=2.7.0,<3.0.0',
 'torch>=1.11.0,<2.0.0',
 'torchaudio>=0.11.0,<0.12.0',
 'torchvision>=0.12.0,<0.13.0',
 'tqdm>=4.62.3,<5.0.0',
 'transformers>=4.17.0,<5.0.0',
 'umap-learn>=0.5.2,<0.6.0']

entry_points = \
{'console_scripts': ['scrap-movies = bechdelai.scripts.scrap_movies:cli']}

setup_kwargs = {
    'name': 'bechdelai',
    'version': '0.0.1a2',
    'description': 'Automating the Bechdel test and its variants for feminine representation in movies with AI',
    'long_description': None,
    'author': 'Data For Good',
    'author_email': 'hellodataforgood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
