# Jack Attack

<br>

A repository for the purposes of learning to create python libraries and implements the JackAttack class.
<br>
Methods for instantiation:
* Install through the Python Package Index
*  Cloning this repository directly


#### PyPi Installation
---
From your command line, run:
<br>
`pip install jackattack`

#### Cloning the Repo
---
In your working directory, use your command line to run:
<br>
`git clone https://github.com/jackrmcshane/jackattack.git`

#### Usage
---
```python
from jackattack import JackAttack

jack = JackAttack()
jack.attack()
...
jack.run()
```

#### Output
---
```
Jack attacks you.
Jack attacks you.
Jack attacks you.
You die.
...
You scare Jack.
He runs away.
```


#### Developing jackattack
---
To install jackattack along with the tools you will need to develop and run tests, run the following in your virtual environment:

```bash
pip install -e .[dev]
```

