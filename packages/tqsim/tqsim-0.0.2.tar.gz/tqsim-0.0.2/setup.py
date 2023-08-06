# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tqsim', 'tqsim.lib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0', 'numpy>=1.23.4,<2.0.0']

setup_kwargs = {
    'name': 'tqsim',
    'version': '0.0.2',
    'description': 'TQSim is a Topological Quantum Computing simulator based on Anyon models',
    'long_description': '<img align="right" width="70" src="https://raw.githubusercontent.com/Constantine-Quantum-Tech/tqsim/main/images/cqtech_logo.png" alt="CQTech">\n\n# TQSim\n\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Constantine-Quantum-Tech/tqsim/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Constantine-Quantum-Tech/tqsim/tree/main)\n[![Version](https://img.shields.io/pypi/v/tqsim?style=flat-square)](https://pypi.org/project/tqsim/)\n[![License](https://img.shields.io/pypi/dm/tqsim?style=flat-square)](https://pypi.org/project/tqsim/)\n[![License](https://img.shields.io/github/license/Constantine-Quantum-Tech/tqsim?style=flat-square)](LICENSE)\n\n\nTQSim stands for Topological Quantum Simulator. It is an open-source library for simulating topological quantum computer based on anyons. \n\n\n## Installation\n\nYou can install TQSim from pip using\n\n```bash\npip install --upgrade tqsim\n```\n\n## Usage\n\n### 1. Basic Example\nIn this example, we create a circuit with 2 qudits, made of 3 anyons each. We then braid the anyons manually.\n```python\nfrom tqsim import AnyonicCircuit\n\ncircuit = AnyonicCircuit(2, 3) # Create a circuit having 2 qudits and 3 anyons per qudits\ncircuit.braid(1, 2) # Braids the first with the second anyon\ncircuit.braid(3, 4) # Braids the first with the second anyon\ncircuit.braid(2, 1)\ncircuit.measure() # Measure the system by fusing the anyons\ncircuit.draw() # Draw the circuit\n```\nHere is the output of the `draw()` method:\n\n![Circuit Output](https://i.ibb.co/3z9pFmQ/example.png)\n\nSimulating the circuit:\n\n```python\ncircuit.run(shots = 50)\n\n```\n\nOutput:\n```bash\n{\'counts\': {\'0\': 16, \'2\': 20, \'4\': 14}, \'memory\': array([4, 2, 2, 2, 2, 2, 2, 4, 2, 4, 2, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4,\n       2, 4, 0, 2, 0, 0, 0, 0, 4, 4, 2, 2, 2, 4, 2, 2, 0, 0, 2, 4, 2, 2,\n       4, 2, 4, 4, 0, 2])}\n```\n\n### 2. Simulating a Hadamard gate\nHere we simulate the application of a Hadamard gate on a single qudit with 3 anyons.\nUnlike the previous example, we will use a braiding sequence of braiding operators and their corresponding powers.\n```python\nfrom tqsim import AnyonicCircuit\n\ncircuit = AnyonicCircuit(nb_qudits=1, nb_anyons_per_qudit=3)  # Create a circuit with 1 qudit composed of 3 anyons\ncircuit.initialize([0,0,1])  # We initialize the circuit in the last state (state 2).\n                            # For this circuit, we have 3 basis states: [0, 1, 2].\n\n# The Hadamard gate braiding sequence in terms of braiding operators\nhad_sequence = [[1, 2], [2, 2], [1, -2], [2, -2], [1, 2], [2, 4], [1, -2], [2, 2],\n                [1, 2], [2, -2], [1, 2], [2, -2], [1, 4]]\n\ncircuit.braid_sequence(had_sequence)  # We apply the braiding sequence.\n                                      # This should put our qudit in a superposition of the states 2 and 1.\ncircuit.measure()  # Measure the system by fusing the anyons\ncircuit.draw()  # Draw the circuit\n```\nThe Hadamard braid looks like this\n\n![Circuit Output](https://i.ibb.co/5kDVWgf/example-hadamard.png)\n\nSimulating the circuit:\n\n```python\nresult = circuit.run(shots = 1000)  # Run the circuit 1000 times.\nprint(result[\'counts\'])  # Show the counts only.\n\n```\n\nOutput:\n```bash\n{\'1\': 493, \'2\': 507}\n```\n\n## Authors and Citation\n*Abdellah Tounsi, Mohamed Messaoud Louamri, Nacer eddine Belaloui, and Mohamed Taha Rouabah – Constantine Quantum Technologies.*\n\nIf you have used TQSim in your work, please use the [BibTeX file](citation.bib) to cite the authors.\n\n## License\n\nCopyright © 2022, [Constantine Quantum Technologies](https://cqtech.org). Released under the [Apache License 2.0](LICENSE).\n',
    'author': 'CQTech.org',
    'author_email': 'constantinequantumtech@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Constantine-Quantum-Tech/tqsim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
