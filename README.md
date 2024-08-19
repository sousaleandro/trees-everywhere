# Trees Everywhere

The project was developed as a technical assessment for the position of Junior Backend Developer. 

## Objective

**Trees Everywhere** aims to create a platform where users from around the world can plant and track trees they have planted virtually. Users can manage accounts, track their planted trees, and view detailed information such as species, location, and age.
  
## Technologies Used
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Setting Up a Virtual Environment
  ```
  python -m venv .venv
  ```
  ```
  source .venv/bin/activate
  ```
## Installing Dependencies
  ```
  pip install -r requirements.txt
  ```
## Starting the Application
  ```
  python manage.py migrate

  ```
  ```
  python manage.py runserver
  ```
## Running Tests
  ```
  pytest
  ```