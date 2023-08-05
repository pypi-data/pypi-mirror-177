# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ez_task',
 'ez_task.config',
 'ez_task.gatherer',
 'ez_task.types',
 'ez_task.types.exceptions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ez-task',
    'version': '0.1.2',
    'description': 'A small package for simple multiprocessing',
    'long_description': "# ez-task - simple python multiprocessing\n\n\nez-task wraps the standard Python multiprocessing library to simplify the management and usage of multiple long-running processes.\nez-task is designed for low-latency applications.\n\n## Installation\n > `pip3 install --no-deps ez-task`\n\n# Usage\n\n\n## Using TaskManager\n```\nfrom ez_task.manager import TaskManager\nimport time\n\ndef foo():\n    time.sleep(1)\n    return 'Foo Call'\n\ndef bar(text):\n    time.sleep(2)\n    return text\n\ndef baz(text, key = 'key'):\n    time.sleep(3)\n    return f'{text} {key}'\n\nwith TaskManager() as manager:\n    foo_task, bar_task, baz_task = manager.define_task_set(foo, bar, baz)\n\n    # Execute tasks concurrently\n    foo_task.run()\n    bar_task.run('bar')\n    baz_task.run('baz', key='booz')\n\n    # Sychronously block for output\n    print('foo task:', foo_task.get_result()) # foo task: foo task Foo\n\n    print('bar task:', bar_task.get_result()) # bar task: bar\n\n    print('baz task:', baz_task.get_result()) # baz task: baz booz\n\n    # Total time taken is 3 seconds\n\n ```\n\n\n## Using Task Directly\n\n```\n\ndef foo(a, b):\n    time.sleep(2)\n    return a + b\n\ntask = Task(foo)\n\nfor i in range(10):\n    task.run(i, i*2)\n\nresults = task.get_all_results()\nprint(results) # [0, 3, 9, 12]\n\n```",
    'author': 'Chris Moyer',
    'author_email': 'chris@telemetry.fm',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
