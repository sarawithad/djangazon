# djangazon
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This web application is the source code for the Bangazon e-commerce web site. It is powered by Python and Django.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)   
- [Contribute](#contribute)
- [Credits](#credits)
- [License](#license)

## About
We are The Illegal Llamas, and we are in the middle of production for a storefront for Bangazon, Llc.

Bangazon is a e-commerce marketplace for users to buy and sell their own physical products. Everything is user-content driven.

### Prerequisites
Install [pip](https://packaging.python.org/installing/)

Install [Python 3.6](https://www.python.org/downloads/)

Install Django:
```
pip install django
```

Install Dependencies:

Install Pillow: ```pip install pillow```

Install Sorl-Thumnail: ```pip install git+https://github.com/mariocesar/sorl-thumbnail.git#egg=sorl-thumbnail```

## Installation
```
git clone https://github.com/illegal-llamas/djangazon.git
cd djangazon
```
Setting up the database:

```
python migrate_llamas.sh
```
Run project in browser:

```
python manage.py runserver
```



## Usage
[UNDER CONSTRUCTION]


## Contribute
1. Fork it!
2. Create your feature branch:
```git checkout -b <YourInititals-WhatNewFeatureDoes>```
3. Commit your changes:
```git commit -m 'Add some feature'```
4. Push to the branch:
```git push origin <YourInititals-WhatNewFeatureDoes>```
5. Submit a pull request :D

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## Credits
Project Manager:
  - [Steve Brownlee](https://github.com/stevebrownlee)

StoreFront Build Contributors:
  * [Harper Frankenstone](https://github.com/hfrankst) - Team Lead
  * [Jordan Nelson](https://github.com/jnelsontn)
  * [Dara Thomas](https://github.com/sarawithad)
  * [Aaron Barfoot](https://github.com/barfootaaron)
  * [Max Baldridge](https://github.com/MaxwellCoriell)

## License
[MIT © Illegal Llamas](./LICENSE)
