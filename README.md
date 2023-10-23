# Django RESTful Web Application

## Overview

The Django RESTful Web Application project is a powerful and versatile application that leverages the Django framework to manage and interact with taxonomy data, protein sequences, proteins, domains, domain coordinates, and their intricate relationships. This application provides a structured and efficient way to create, retrieve, update, and delete data related to biological taxonomy and protein information. It ensures data integrity while offering a user-friendly experience for managing complex biological data.

## Table of Contents

- [Data Models](#data-models)
- [Django Admin Configuration](#django-admin-configuration)
- [Database Population](#database-population)
- [Serializers](#serializers)
- [API Endpoints](#api-endpoints)
- [Unit Testing](#unit-testing)
- [Getting Started](#getting-started)

## Data Models

The project begins by defining comprehensive data models that represent various entities related to biological taxonomy and proteins. These models include:
- Proteins
- Protein Sequences
- Domains
- Domain Coordinates
- Taxonomy

The relationships between these models are structured to maintain data integrity.

## Django Admin Configuration

The Django Admin interface is configured to provide an intuitive and user-friendly way to manage the database. Admin classes are defined for each model, allowing for easy creation, editing, and deletion of records.

## Database Population

Data from CSV files is efficiently loaded into the database using a Python script. This ensures that the application starts with relevant and structured data.

## Serializers

Custom serializer classes are implemented for each model to facilitate data conversion, validation, and processing. Serializers handle data conversion to and from JSON format, data validation, and data processing, ensuring data integrity and consistency.

## API Endpoints

The application exposes RESTful API endpoints to interact with taxonomy data, protein information, and domain details. These endpoints provide a means to retrieve detailed information and perform actions such as adding new records.

- `taxonomy_detail`: Retrieve taxonomy details and related data.
- `add_record`: Add new records, including taxonomy, proteins, and domains.
- `protein_detail`: Retrieve detailed protein information.
- `pfam_detail`: Get Pfam domain details.
- `coverage`: Calculate protein coverage details.

## Unit Testing

Comprehensive unit tests are conducted to verify the functionality and validity of the application. These tests cover a range of scenarios, including successful operations and cases with invalid or missing data.
