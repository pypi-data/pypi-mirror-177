# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['streamlit_pills']

package_data = \
{'': ['*'],
 'streamlit_pills': ['frontend/*',
                     'frontend/build/*',
                     'frontend/build/static/js/*',
                     'frontend/public/*',
                     'frontend/src/*']}

install_requires = \
['streamlit>=1.12.0,<2.0.0']

setup_kwargs = {
    'name': 'streamlit-pills',
    'version': '0.1.0',
    'description': '💊 A Streamlit component to show clickable pills/badges',
    'long_description': '# streamlit-pills 💊\n\n[![PyPI](https://img.shields.io/pypi/v/streamlit-pills)](https://pypi.org/project/streamlit-pills/)\n\n**A Streamlit component to show clickable pills/badges.**\n\nThis custom component works just like `st.selectbox` but shows the options as clickable \npills. It\'s nice to show the user upfront what they can select, without going through a \ndropdown.\n\n---\n\n<h3 align="center">\n  💊 <a href="https://pills.streamlit.app/">Demo app</a> 💊\n</h3>\n\n---\n\n<p align="center">\n    <a href="https://pills.streamlit.app/"><img src="images/demo.png"></a>\n</p>\n\n\n## Installation\n\n```bash\npip install streamlit-pills\n```\n\n## Usage\n\n```python\nfrom streamlit_pills import pills\nselected = pills("Label", ["Option 1", "Option 2", "Option 3"])\nst.write(selected)\n```\n\nSee [the demo app](https://pills.streamlit.app/) for a detailed guide!\n\n\n## Development\n\nNote: you only need to run these steps if you want to change this component or \ncontribute to its development!\n\n### Setup\n\nFirst, clone the repository:\n\n```bash\ngit clone https://github.com/jrieke/streamlit-pills.git\ncd streamlit-pills\n```\n\nInstall the Python dependencies:\n\n```bash\npoetry install\n```\n\nAnd install the frontend dependencies:\n\n```bash\ncd streamlit_pills/frontend\nnpm install\n```\n\n### Making changes\n\nTo make changes, first go to `streamlit_pills/__init__.py` and make sure the \nvariable `_RELEASE` is set to `False`. This will make the component use the local \nversion of the frontend code, and not the built project. \n\nThen, start one terminal and run:\n\n```bash\ncd streamlit_pills/frontend\nnpm start\n```\n\nThis starts the frontend code on port 3001.\n\nOpen another terminal and run:\n\n```bash\ncp demo/streamlit_app.py .\npoetry shell\nstreamlit run streamlit_app.py\n```\n\nThis copies the demo app to the root dir (so you have something to work with and see \nyour changes!) and then starts it. Now you can make changes to the Python or Javascript \ncode in `streamlit_pills` and the demo app should update automatically!\n\nIf nothing updates, make sure the variable `_RELEASE` in `streamlit_pills/__init__.py` is set to `False`. \n\n\n### Publishing on PyPI\n\nSwitch the variable `_RELEASE` in `streamlit_pills/__init__.py` to `True`. \nIncrement the version number in `pyproject.toml`. Make sure the copy of the demo app in \nthe root dir is deleted or merged back into the demo app in `demo/streamlit_app.py`.\n\nBuild the frontend code with:\n\n```bash\ncd streamlit_pills/frontend\nnpm run build\n```\n\nAfter this has finished, build and upload the package to PyPI:\n\n```bash\ncd ../..\npoetry build\npoetry publish\n```\n\n## Changelog\n\n### 0.1.0 (November 22, 2022)\n- Initial version\n',
    'author': 'Johannes Rieke',
    'author_email': 'johannes.rieke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
