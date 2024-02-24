# Project 1

Application Web de critique de livres permettant aux utilisateurs de donner des notes à des livres celebres<br>
Technologies utilisées:lo
## Project stack 
| Stack | Logo |
| ----- | ---- |
| Docker| <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>     |
| Flask | <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a>
| PostgreSQL |<a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> |


## Installation
1. Clone the repository: `git clone https://github.com/bambadiagne/project1.git`

2. Create .env file copy .env.sample contents and change the values
3. You can use the docker-compose file it's so simple but you need that Docker installed in your device

```bash
docker-compose up -d
```
4. You can generate data by running  <a href="./blog/import.py" target="_blank" rel="noreferrer"> import.py</a>  script who contains 5k books rows in csv file.
Enter inside app container and run import.py under blog directory