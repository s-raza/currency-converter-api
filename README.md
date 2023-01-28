# Currency Converter App using React+FastAPI+Docker+NGINX+Kubernetes
[![Sphinx Documetation](https://img.shields.io/badge/Docs-Sphinx-005571?style=flat-square)](https://s-raza.github.io/currency-converter-api/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-005571?style=flat-square&logo=react)](https://reactjs.org/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-005571?style=flat-square&logo=pre-commit)](https://pre-commit.com/)
[![Async](https://img.shields.io/badge/Async-005571?style=flat-square&logo=python)](https://docs.python.org/3/library/asyncio.html)
[![Redis](https://img.shields.io/badge/Redis-005571?style=flat-square&logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-005571?style=flat-square&logo=docker)](https://www.docker.com/)
[![SQLAlchemy-MySQL](https://img.shields.io/badge/MySQL-SQLAlchemy-005571?style=flat-square&logo=mysql)](https://www.sqlalchemy.org)
[![NGINX](https://img.shields.io/badge/NGINX-005571?style=flat-square&logo=nginx)](https://www.nginx.com/)
<img src="https://img.shields.io/badge/REST--API-005571?style=flat-square"/>
<img src="https://img.shields.io/badge/Microservices-005571?style=flat-square"/>
<img src="./gh-static/06-react-ui.gif"/>
<br>

**React+FastAPI+NGINX based currency converter app with micro services architecture implemented using Docker and Kubernetes.**

&check; FastAPI backend | &check; React front end for a currency converter | &check; Token based authentication with Username and Password | &check; Async | &check; Micro Services | &check; Tests Automation | &check; CI/CD Ready | &check; REST API | &check; Redis Cache | &check; SQLAlchemy/MySQL


# Documentation

Code documentation and instructions on how to run the application can be viewed
on the project's [GitHub Pages](https://s-raza.github.io/currency-converter-api/).
The code documentation is pre-built using [Sphinx](https://www.sphinx-doc.org/en/master/)

Alternatively the code documentation can be read directly from the docstrings in the source code.

# React Frontend

## Login Interface

<img src="./gh-static/04-login-page.jpg"/>
<br>

Sign in with pre-defined credentials user:pass123

<img src="./gh-static/05-currency-converter.jpg"/>
<br>

The currency converter is accessible after a successful login.

# FastAPI Backend

## API Documentation

The API documentation is available at `http://localhost:8080/docs`

**Swagger UI API Docs**
<img src="./gh-static/01-api-docs.jpg"/>
<br>

## Authentication for Swagger UI

The API requires authentication. A default user with credentials `user:pass123` is added to the
database when the Currency API service starts.

**Swagger UI Login Dialog**
<img src="./gh-static/02-user-auth-dialog.jpg"/>
<br>


**Swagger UI Successful Login**
<img src="./gh-static/03-user-authorized-dialog.jpg"/>
<br>

## Planned Updates

1. Add a caching middleware layer using Redis running in a separate container. &check;
2. Implement Kubernetes for deployment. &check;
3. Use nginx container for deployment. &check;
4. Add more endpoints. E.g.

    1. Highest/Lowest rate for a currency on a given day
    2. Highest/Lowest rate for a currency between two dates.
    3. Latest rates of all currencies with reference to a   base currency. &check;

5. Interactive front end for a currency converter using React. &check;
6. Interactive front end to visualize trends in currency rates using React.
7. Closer integration of Pydantic and SQLAlchemy models in FastAPI.
