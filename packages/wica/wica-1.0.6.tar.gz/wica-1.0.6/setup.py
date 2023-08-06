# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wica']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'wica',
    'version': '1.0.6',
    'description': 'A simple python API to access wica-http SSE.',
    'long_description': '# PyWica - Wica Python API \n[![coverage report](https://git.psi.ch/proscan_data/py-wica/badges/main/coverage.svg)](https://git.psi.ch/proscan_data/py-wica/-/commits/main)\n[![pipeline status](https://git.psi.ch/proscan_data/py-wica/badges/main/pipeline.svg)](https://git.psi.ch/proscan_data/py-wica/-/commits/main)\n#### Table of Contents\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [Quick-start Guid](#quick-start-guide)\n- [Documentation](#documentation)\n- [Dependencies](#dependencies)\n- [Contribute](#contribute)\n- [Project Changes and Tagged Releases](#project-changes-and-tagged-releases)\n- [Developer Notes](#developer-notes)\n- [Contact](#contact)\n\n# Introduction\nThis project/package aims to provide a simple python interface to the wica-http server.\nCheck out the async branch to get the async version of the package\n\n# Installation\nInstall with pip\n```bash\npip install wica\n```\n# Quick-start Guide\n```python\nimport asyncio\nimport time\n\nfrom wica import WicaStream\n\n\nasync def simple_example_blocking_io():\n    """A simple example of how to use WicaStream.\n\n    In this example we are using asyncio, but you could use any other concurrency or parallel processing package,\n    you just need the ability to interrupt the stream somehow!\n    Check out the async version of this package!\n    """\n\n    wica_stream = WicaStream(base_url="http://student08/ca/streams", channels=["MMAC3:STR:2"])\n\n    def run_stream():\n        wica_stream.create()\n        for message in wica_stream.subscribe():\n            print(message)\n\n    def stop_stream():\n        print("Starting to wait")\n        time.sleep(5)\n        print(wica_stream.destroy())\n\n    # The following functions put the blocking functions into their own thread.\n    async def thread_run_stream():\n        return await asyncio.to_thread(run_stream)\n\n    async def thread_stop_stream():\n        return await asyncio.to_thread(stop_stream)\n\n    return await asyncio.gather(thread_run_stream(), thread_stop_stream())\n\nasync def main():\n    await simple_example_blocking_io()\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n# Documentation\nCurrent Features:\n* Custom Client to handle be able to extract last line of SSE with timestamp and message type.\n* Simple functions to create, delete and subscribe to streams\n* Blocking IO (non-blocking versions available in async branch)\n\nCheck out the [wiki](https://proscan_data.gitpages.psi.ch/py-wica) for more info!\n\n# Dependencies\n* requests\n\n# Contribute\nTo contribute, simply clone the project.\n\n# Project Changes and Tagged Releases\n* See the Changelog file for further information\n* project releases are available in pypi\n\n# Developer Notes\nCurrently None\n\n# Contact\nIf you have any questions pleas contact \'niklas.laufkoetter@psi.ch\'\n',
    'author': 'Niklas Laufkoetter',
    'author_email': 'niklas.laufkoetter@psi.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://git.psi.ch/proscan_data/py-wica',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
