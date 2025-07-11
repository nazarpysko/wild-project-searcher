
<h1 align="center">
  <br>
  <a href="http://twps.cub3.xyz"><img src="/img/wild-project-logo.png" alt="The Wild Project Searcher" width="200"></a>
  <br>
  The Wild Project Searcher
  <br>
</h1>

<h4 align="center">A semantic searcher for podcasts transcription.</h4>

<p align="center">
  <a href="#summary">Summary</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a>
</p>

![screenshot](/img/screenshot.png)

## Summary

This is a project for the Cloud Computing subject of the Inteeligent Systems Master of Universitat Jaume I. It consists in a semantic searcher for podcast transciptions. The application is deployed in 3 different containers:
* An elastic search container that stores the indexes of the transciptions and is responsible for finding the search rsults.
* A Flask backend implementing the API using REST methodology that is in charge of the NLP model.
* A Vue front-end for searching and visualizing the results.

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com) and [Docker](https://www.docker.com/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/nazarpysko/wild-project-searcher

# Go into the repository
$ cd wild-project-searcher

# Run the app
$ docker compose up -d

# Initialize the indices
$ docker exec -ti backend-wild-project python init_podcasts.py
```

Now you can acces the app through `http://localhost:8080`

To make it available through a public IP you could use a reverse proxy. Be aware that the URL used by the frontend to contact the API and fetch the results should be changed in this case. It is located at `Web/src/services/index.ts`.

## Credits

This software uses the following open source packages:

- [Docker](https://www.docker.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Vue](https://vuejs.org/)
- [Elasticsearch](https://www.elastic.co/es/elasticsearch)
- [Nginx](https://www.nginx.com/)
