# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqvis']

package_data = \
{'': ['*'], 'gqvis': ['template/*']}

install_requires = \
['ipython==7.34.0', 'neo4j>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'gqvis',
    'version': '0.1.6',
    'description': 'A simple package for visualising the results of a cypher-based graph query to Neo4j in Python.',
    'long_description': '# GQVis\n\nA simple package for visualising the results of a graph query (to Neo4j) in an interactive Python environment (such as Jupyter notebook).\n\n![Screenshot of an example graph](https://github.com/nlp-tlp/gqvis/blob/main/image_1.png?raw=true)\n\n## Installation\n\nSimply run:\n\n    pip install gqvis\n\n## Usage\n\nFirst, import the package via\n\n    import gqvis\n\nThere are two ways to use this package, detailed below.\n\n### Visualising the result of a Neo4j Cypher query\n\nThe first way to use the class is to visualise the result of a Neo4j Cypher query. This requires you to have a Neo4j database running.\n\nYou must first create an environment variable called `NEO4J_PASSWORD` and set the value of this variable to the password of your Neo4j graph. In Jupyter, you can simply do:\n\n    %env NEO4J_PASSWORD=password\n\nThe default password is \'password\', so if your Neo4j graph already has this password there is no need to set this variable.\n\nThen, you can run the following:\n\n    gqvis.visualise_cypher(\'MATCH (n1:Entity)-[r]->(n2:Entity) RETURN n1, r, n2 LIMIT 500\')\n\nNote that unlike Neo4j, which has the \'connect result nodes\' option to automatically connect nodes that have relationships, you will need to return the relationships explicitly in your query. Only relationships in the `RETURN` statement will be visualised.\n\n### Visualising nodes and links directly\n\nYou can also visualise a given list of nodes and edges - No Neo4j required. For example:\n\n    nodes = [\n        {\n          "id": 1,\n          "category": "Person",\n          "name": "Bob",\n        },\n        {\n          "id": 2,\n          "category": "Food",\n          "name": "Jelly",\n        },\n        {\n          "id": 3,\n          "category": "Person",\n          "name": "Alice",\n        }\n    ]\n    links = [\n        {\n          "source": 1,\n          "target": 2,\n          "type": "EATS",\n        },\n        {\n          "source": 3,\n          "target": 1,\n          "type": "LIKES",\n        },\n    ]\n    gqvis.visualise_list(nodes, links)\n\nThis will create a graph visualisation with three nodes ("Bob", "Jelly", "Alice"), and two links (Bob eats Jelly, Alice likes Bob). You can have other properties (such as `"age": 45` on Bob) - they\'ll be shown in the tooltip when hovering over a node.\n\nThe `"id"`, `"category"` and `"name"` properties are required on each node. The `"name"` property is what will be written on the nodes in the visualisation, while the `"category"` will determine their colour (more on this below).\n\nFor the links, `"source"` is the id of the source node, `"target"` is the id of the target node, and `"type"` is the type of relationship. These are all required.\n\n### About the visualisation\n\nNodes are coloured based on the `category` property.\n\nFor the Cypher visualisation, the way the graph decides on the colour of each node is based on the last label of that node, i.e. if a node had the following labels:\n\n    Entity, Item\n\n... it would be coloured based on the `Item` label. The colours are determined automatically, i.e. each category receives its own unique colour.\n\n## Notes\n\nWe use the dependency `neo4j` (the Neo4j driver for Python) rather than `py2neo` because it turns out `py2neo` does not output the exact same results as Neo4j. The way this whole thing works is by creating a list of nodes from all node objects returned by the cypher query, then creating links (by linking nodes via their ids). It didn\'t seem possible in `py2neo`, but was pretty straightforward with the `neo4j` package.\n\nYou can run `src/template/template.html` by itself (i.e. open it directly in Firefox/Chrome) for development purposes. When running it this way, it will be populated by some dummy data specified in `src/template/dummyData.js`.\n\nNote that you must have an internet connection to use this package at the moment as it pulls D3.js from an online CDN.\n',
    'author': 'Michael Stewart',
    'author_email': 'michael.stewart.webdev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
