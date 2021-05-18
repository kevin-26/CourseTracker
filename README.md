<h3 align="center">SubmitMQ</h3>

<div align="center">


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
<br>



</div>

------------------------------------------

> Due to the pandemic, all educational institutions have been shut down since early 2020 and the entire education system has shifted online; e-learning has been at the forefront since the commencement of lockdown. Hence, there are multiple e-learning platforms that are commonly used by professors: MS Teams, Google classroom and LMS. Naturally, it becomes difficult for students to keep a track of all assignments and resources posted on these platforms. Hence, we aim to scrape relevant data from these platforms and display it to users via a single application.

------------------------------------------

<br>

<div align="center">
    <h3>Architecture/Event flow<h3>
</div>

<div align="center">
<a href="https://ibb.co/tsCYy81"><img src="https://i.ibb.co/2tKcXgp/image.png" alt="architecture" border="0"></a>
</div>
<br>

The project uses selenium and beautifulsoup4 for web automation and scraping. A flask server is setup for webapp communication
The server sends the data to the frontend in various views

#### Tech stack
- Frontend - HTML, CSS, JavaScript, Bootstrap
- Backend - Flask, Selenium, Beautifulsoup4 

<div align="center">
    <h3>Client<h3>
</div>

<div align="center"><h5> Home </h5>
The Home page displays all the subjects along with the latest 2 resources and assignments (if not submitted)
</div>

<div align="center">
<a href="https://ibb.co/tsCYy81"><img src="https://i.ibb.co/2tKcXgp/image.png" alt="Home" border="0"></a>
</div>

<div align="center"><h5> Subject View </h5>
The Subject page displays resources and assignments of the selected subject
</div>
<div align="center">
<a href="https://ibb.co/tsCYy81"><img src="https://i.ibb.co/2tKcXgp/image.png" alt="Subject" border="0"></a>
</div>

<div align="center"><h5> Assignment View </h5>
The Assignment page displays all the pending assignments of all the subjects
</div>
<div align="center">
<a href="https://ibb.co/tsCYy81"><img src="https://i.ibb.co/2tKcXgp/image.png" alt="Assignment" border="0"></a>
</div>


#### Using API endpoints

```
GET /home: Get details for all the subjects 

GET /subject/<string:id>: Get info about the specific subject

GET /home: Get details for all the subjects 

GET /assignments: Get info about all the pending submissions

POST /assignments/<assignment:id>: Submit a file for the specific assginment(valid for LMS submission)

```

<div align="center">
    <h3>Future work<h3>
</div>

- [ ] Integrating MS Teams
- [ ] Add pagination in frontend
- [ ] Adding submissions for google classroom
- [ ] Building a 3 layer architecture
- [ ] Notify users when assignment is submitted
- [ ] Add logging

<div align="center">
    <h3>Requirements</h3>
</div>
All the requirements of the project are available in requirements.txt file


<div align="center">
    <h3>Running the project locally<h3>
</div>

Setup the server:

```
pip install -r requirements.txt
```

Setting up the environment:
On Linux:
```
$ set FLASK_APP="app:app"
$ set FLASK_ENV="development"
```
On Windows:
```
$ set FLASK_APP="app:app"
$ set FLASK_ENV="development"
```

Running the flask server (in no reload mode - in normal mode the server is buggy):
```
$ flask run --no-reload
```

Login credentials and selecting valid subjects
```
$ flask run --no-reload
```

The client can be viewed at 5000 port


#### ...but why would I use this?

This isn't a completed project. It's far from done. But the future work of the project can act as a single client for some of the learning management systems available right now.
