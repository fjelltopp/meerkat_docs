===================
Meerkat Frontend
===================

The purpose of Meerkat Frontend is to present Meerkat's data for analysis and surveilance.  It does this through a series of web pages. At the heart of the frontend is the "Technical Site", which offers the most complete means to explore the data through a large array of selection tools and graphs. The frontend has several components though, and has been built by multiple people.   

------------------
Components
------------------

* The Homepage gives a quick overview of the project for any interested parties. This includes: some text describing the project, a dynamically updated map showing where the data is coming from, and some dynamically updated key indicators for the project. The indicators we show are the total number of: consultations, cases, facilities and alerts in the data.

* The Reports Pages generate neat detailed summaries of the data in the system that can be shared publicly with other people. Weekly reports are generated for all different location levels from the country to the clinic. 

* The technical site displays detailed information and is only accesible with a password. It can display data on all location levels from the country to the individual clinic, and includes demographics, disease distributions, geographical distributions and epi-curves.

------------------
Structure
------------------

Meerkat Frontend is structured as a Python Flask app, and as such, is primarily made up of static assets, Jinja2 templates and Python modules. The static assets are assembled from the "src" folder and the "bower_components" folder using Gulp. Further folders and files exist to manage the app's testing, and to abstract country specifics into configuration files. The whole thing is further structured so it can be bundled up as a python package.  Here's some information regarding particular core files and folders of note:

runserver.py - Runs the development/testing server for the app. 

config.py - Specifies a host of configuration variables used throughout Meerkat Frontend.  Allows you to distinguish between a development,testing and production environment.

homepage_<country>.json - These files include the homepage data for each country.  The homepage is built around the data specified in these files. Abstracting this data into a seperate file means it is easier to replicate for multiple countries.

meerkat_frontend/

 __ Common.py - A file containing a number of python methods that could be useful across all components.

 __ apiData /  A folder containing data for a static API, used for testing and development instead of the live API.

 __ test / A folder  containing our testing harness for Meerkat_Frontend


----------------------------
Documentation
----------------------------
To see the specific  `documentation`_.

.. _documentation: frontend/modules.html 
