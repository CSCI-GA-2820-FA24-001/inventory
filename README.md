# NYU DevOps Inventory Team Documentation

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
![workflow](https://github.com/CSCI-GA-2820-FA24-001/inventory/actions/workflows/ci.yml/badge.svg)
[![Coverage Status](https://codecov.io/gh/CSCI-GA-2820-FA24-001/inventory/branch/master/graph/badge.svg?token={token})](https://codecov.io/gh/CSCI-GA-2820-FA24-001/inventory)

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

- GET /inventory: List all inventory items, with optional query parameters for filtering based on item name, quantity range, condition, and stock level.
  - Query Parameters
    - `name`: Filter by inventory item name
    - `quantity_min` and `quantity_max`: Filter items with quantities within a specified range
    - `condition`: Filter by item condition (e.g., NEW, OPENBOX, USED)
    - `stock_level`: Filter by stock level (e.g., IN_STOCK, LOW_STOCK, OUT_OF_STOCK)
  - Example Usage
    - Filter by name: `curl -X GET "http://localhost:5000/inventory?name=widget"`
    - Filter by quantity range: `curl -X GET "http://localhost:5000/inventory?quantity_min=10&quantity_max=50"`
    - Filter by condition: `curl -X GET "http://localhost:5000/inventory?condition=USED"`
    - Filter by stock level: `curl -X GET "http://localhost:5000/inventory?stock_level=OUT_OF_STOCK"`    
- POST /inventory: Create a new inventory item
- GET /inventory/\<id\>: Retrieve a specific inventory item by ID
- PUT /inventory/\<id\>: Update a specific inventory item by ID
- DELETE /inventory/\<id\>: Delete a specific inventory item by ID
- PUT /inventory/\<id\>/restock/\<quantity\>: Adjust the stock quantity of a specific inventory item by adding or subtracting a specified quantity. Positive values increase the stock, while negative values decrease it, as long as the resulting quantity remains non-negative.
  - Query Parameters
    - `id`: The unique identifier of the inventory item to restock.
    - `quantity`: The quantity to adjust for the inventory item. Positive values increase stock, while negative values decrease it.
  - Example Usage
    - To increase the stock of an item by 10 units: `curl -X PUT "http://localhost:5000/inventory/1/restock/10"`
    - To decrease the stock of an item by 5 units (ensure it doesn’t make the quantity negative): `curl -X PUT "http://localhost:5000/inventory/1/restock/-5"`

### Setup and Usage
1. Install dependencies.
2. Initialize the database using SQLAlchemy.
3. Implement the REST API functionality in routes.py.

## Steps to run application on a Kubernetes cluster

1. Create a Kubernetes cluster using the make recipe `make cluster`
2. Build the Docker image using the command `docker build -t inventory:latest .`
3. Tag the Docker image using the command `docker tag inventory:latest cluster-registry:5000/inventory:latest`
4. Push the Docker image to the local registry using the command `docker push cluster-registry:5000/inventory:latest` 
Note: If the push fails, it is likely because your
`/etc/hosts` file is not configured correctly. You can add the following line to your `/etc/hosts` file: `"127.0.0.1 cluster-registry"`
1. Apply k8s manifests using the command `kubectl apply -f k8s/`
2. Check the status of the pods using the command `kubectl get pods`. When both pods are in the `Running` state, the application is ready to use on `localhost:8080`

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
