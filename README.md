# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)


## Overview

This project is the implementation of inventory function under an E-Commerce platform, being developed for the NYU course DevOps & Agile Methodologies. The `/service` folder contains `models.py` file for the model and a `routes.py` file for the service. The `/tests` folder has test case starter code for testing the model and the service separately. For functionality implemenation, we refered to the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
pyproject.toml      - Poetry list of Python libraries required by your code

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - configuration parameters
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── cli_commands.py    - Flask command to recreate all tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/                     - test cases package
├── __init__.py            - package initializer
├── factories.py           - Factory for testing with fake objects
├── test_cli_commands.py   - test suite for the CLI
├── test_models.py         - test suite for business models
└── test_routes.py         - test suite for service routes
```

## REST API
This project provides a REST API for managing an inventory system, allowing for creating, reading, updating, and deleting inventory items.

### Models
The models.py file defines the data model for the Inventory. It uses SQLAlchemy for ORM (Object-Relational Mapping). The key components of the model include:

- Inventory: Represents an inventory item with fields for:
  - id: Unique identifier (primary key)
  - name: Name of the inventory item
  - quantity: Quantity of the item
  - condition: Condition of the item (e.g., new, used)
  - stock_level: Stock level description (e.g., in stock, out of stock)

It also includes methods for basic CRUD (Create, Read, Update, Delete) operations, as well as serialization/deserialization for working with JSON data.

### API Endpoints
The routes.py file defines the endpoints for the Inventory API. Currently, placeholders are present, and further implementation is needed. The API endpoints include:

- GET /inventory: List all inventory items
- POST /inventory: Create a new inventory item
- GET /inventory/<id>: Retrieve a specific inventory item by ID
- PUT /inventory/<id>: Update a specific inventory item by ID
- DELETE /inventory/<id>: Delete a specific inventory item by ID

### Setup and Usage
1. Install dependencies.
2. Initialize the database using SQLAlchemy.
3. Implement the REST API functionality in routes.py.

License
This project is licensed under the Apache License 2.0. See the LICENSE file for more details.

## License

Copyright (c) 2016, 2024 [John Rofrano](https://www.linkedin.com/in/JohnRofrano/). All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the New York University (NYU) masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by [John Rofrano](https://cs.nyu.edu/~rofrano/), Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.

The team members are:
- [Shiwei He](https://www.linkedin.com/in/shiweihe0713/)
- [Haozhou Huang](https://www.linkedin.com/in/haozhou-huang/)
- [Haardik Dharma](https://www.linkedin.com/in/haardik-dharma/)
- [Chengying Wang](https://www.linkedin.com/in/chengying-wang-03b85924a/)
- Jesse Liu