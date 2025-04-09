<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ClassX-Image-Classification-Project/ClassXTool">
    <img src="static/images/Logos/ClassX Logo White.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">ClassXTool</h3>

  <p align="center">
    An automatic image training datasets labeling tool for multi-domain AI/ML research
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Project Background
Due to climate change, various disasters including flooding, drought, wildfire, and air quality have become a national and global pressing challenge. AI and ML approaches have been used to build models to simulate and answer questions in a ChatGPT fashion. However, lacking large amounts of high-quality training datasets, the adoption of AI/ML for addressing climate change issues is hampered. this project will produce a commercial prototype that can enable production of sizable and high-quality training datasets in an automatic and timely fashion.

This project aims to develop an automatic image training datasets labeling tool for multi-domain AI/ML research.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![NGINX][NGINX]][NGINX-url]
* [![Keycloak][Keycloak]][Keycloak-url]
* [![React][React.js]][React-url]
* [![Flask][Flask]][Flask-url]
* [![Celery][Celery]][Celery-url]
* [![MySQL][MySQL]][MySQL-url]
* [![Redis][Redis]][Redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- Docker Engine
- Conda
- Python



### Installation for Devs

1. Install the [Docker Engine](https://docs.docker.com/engine/install/)
2. Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
3. Clone the repo
   ```sh
   git clone https://github.com/ClassX-Image-Classification-Project/ClassXTool.git
   ```

4. Create `.env`
   ```js
      SECRET_KEY = ''
 
 
      CLASSX DATABASE
      HOST = 'dbx'
      MYSQL_ROOT_USER = 'root'
      MYSQL_ROOT_PASSWORD = ''
      DB_USER = 'user'
      DB_PASSWORD = ''
      DB_PORT = '3306'
      DB = 'label_db'
      
      # KEYCLOAK DATABASE
      OAUTH_DB = 'keycloak_db'
      
      # KEYCLOAK/OAUTH
      KEYCLOAK_ADMIN_PASSWORD = ''
      OAUTH_SECRET = ''
      KEYCLOAK_HOST_URL = 'http://localhost:8080'
      KEYCLOAK_HOSTNAME = 'localhost'
      KC_DEV = 'start-dev'
      KC_SOURCE_URL = 'http://kcx:8080/'
      KC_REALM = 'STC-ClassX-DEV'
      KC_REALM_CLIENT = 'flask-app'
      
      # FLASK
      FLASK_ENV = 'development'
      JWT_SECRETE_KEY = ''
      ADDRESS = 'http://appx:5000'
      ADMIN_CLIENT_ID = 'admin-api'
      ADMIN_CLIENT_SECRET =  ''
      
      WEBSITE_NAME = "ClassX"
      HOMEPAGE_ABOUT = 'Multi-Stage Build'
      WEBSITE_EMAIL = 'example@email.com'
      WEBSITE_LOGO = 'static/images/Logos/nasa-logo-png-nasa-logo.png'
      
      CELERY_REDIS_URL = 'redis://redis:6379/0'

      # DOCKER
      CONTAINERS = 'dbx, appx, kcx, worker, redis'
   ```

5. Install Conda environment (Local)
```sh
conda env create -f stable_env.yml
```

6. Build Docker environment
```sh
docker compose -f dev.yml build
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

We'll be leveraging internal python script to manage our Docker environment. This makes it easier for devs to work with containers by abstracting Docker's complexities.

_For more info, we advise you read through the [Docker Environment Manager Documentation](https://github.com/ClassX-Image-Classification-Project/ClassXTool/blob/test/envmgr-doc.md)_

1. Launch local Docker environment
```sh
docker compose -f dev.yml up
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/ClassX-Image-Classification-Project/ClassXTool/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Theodore Spanbauer - tspanbau@gmu.edu

Project Link: [https://github.com/ClassX-Image-Classification-Project/ClassXTool](https://github.com/ClassX-Image-Classification-Project/ClassXTool)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Gian Sung - System Administrator](https://github.com/jglsung)



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members

[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers

[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues

[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username

[product-screenshot]: images/screenshot.png

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/

[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/

[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/en/stable/

[MySQL]: https://img.shields.io/badge/MySQL-grey?style=for-the-badge&logo=mysql
[MySQL-url]: https://www.mysql.com/

[Celery]: https://img.shields.io/static/v1?style=for-the-badge&message=Celery&color=37814A&logo=Celery&logoColor=FFFFFF&label
[Celery-url]: https://docs.celeryq.dev/en/stable/getting-started/introduction.html

[NGINX]: https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white
[NGINX-url]: https://nginx.org/en/

[Redis]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/

[Keycloak]: https://img.shields.io/badge/Keycloak-4D4D4D?logo=keycloak&logoColor=fff&style=for-the-badge
[Keycloak-url]: https://www.keycloak.org/