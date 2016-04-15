===================
Meerkat Frontend
===================

**Meerkat Frontend** presents the data drawn from **Meerkat API** and **Meerkat Abacus** in a web app.   It has been designed in collaboration with our various stakeholders to meet their speicifc needs (most notably the Jordinian Ministry of Health). At the heart of the frontend is the "Technical Site", which offers the most complete means to explore the data through a large array of tools, including a "dashboard" of tables and charts, auto-generated summary reports, an alerts notification service, and specialist tools for visualisaing and downloading data. 

------------------
Components
------------------

* **The Homepage** gives a public brief overview of the specific country's project, and acts as a splash page to the secured technical site. This includes: some text describing the project, a dynamically updated map showing where the data is coming from, and some dynamically updated key indicators for the project.

* **The Technical Dashboard** displays detailed information and is only accesible with a password. It can display data for any selected location from the country to the individual clinic, and includes pages showing demographics, disease distributions, geographical distributions and epi-curves.

* **The Reports** component generates neat detailed summaries of the data in the system that can be shared publicly with other people. Weekly reports can be generated for user's desired time period and location. 

* **The Notifications** or **Messaging** service subscribes users to receive email and sms updates of system alerts and reports. The messages are sent by our purpose built Meerkat Hermes module, controlled through a secured REST API. 

* **The Explore Data** component allows users to draw and export the tables and charts that they want to see, picking which categories to show along each access and filtering/ording the records as they desire. 

* **The Download Data** component provides a means of downloading pre-pared data sets and any raw data that the user desires for their own analysis.

------------------
Structure
------------------

As a Python flask app, Meerkat Frontend is made up of static assets, Jinja2 templates and Python modules.  Further folders and files exist to manage the app's testing, and to abstract country specifics into configuration files, and bundle it up as a python package.  

Meerkat Frontend depends upon three package management systems: Python's PIP, Javascript's Node Package Manager (NPM) and the client-side package manager Bower.  The dependieces required from each package manager are stored in the files **setup.py**, **package.json** and **bower.json** respectively. After pulling the repository from **GitHub**, the following commands need to be run from the package's root folder to install the necessary dependancies, ``python setup.py install``, ``npm install``, and ``bower install``. 

One of the packages installed by NPM is the build tool **Gulp**. Gulp performs a number of build-related processes specified in the file **gulp.js**. Among other things Gulp optimises images, builds the SASS files into CSS files, runs **JSHint** on the Javascript, draws all the Javascript and CSS files together into large single files (reducing the number of requests to load a web page), cleans out our static assets folder, and then re-assembles the updated static assets ready to be used. *NOTE:* static assets are assembled from the **meerkat_frontend/src** folder, **bower_components** folder and **node_modules** folder, and then placed in the **meerkat_frontend/static** folder; *there is no need to directly edit anything in the static assets folder*.  In order to run Gulp, you must first clean the static assets using the **clean** task specified in gulp.js, we therefore suggest using the following command to build the project ``gulp clean && gulp``. 

Files and folders of particular note include:

**runserver.py** - Runs a development/testing server for the app. Note that it is advised to run this inside the development or production environments built in the Meerkat Infrastructure repository. 

**config.py** - Specifies a host of configuration variables used throughout Meerkat Frontend.  Allows you to distinguish between a development,testing and production environment.

**meerkat_frontend/**

   **common.py** - A file containing a number of python methods that could be useful across all components.

   **apiData/**  A folder containing data for a static API, used for testing and development instead of the live API.

   **test/** A folder containing our testing harness for Meerkat_Frontend

   **views/** A folder containing the python flask view modules. There is a different view for each component.  This is where much of the server-side work happens.

   **templates/** A folder containing Jinja2 templates that are rendered in the Python view files.  There is a seperate folder of templates for each component.  

      **base.html** A file containing the base template that is extended by other templates in each component. Jinja2 templates are hereditary, reducing the need to re-write the same bits of template multiple times. This base tamplate includes the header, footer, navigation bar and other core fragments of layout etc...

      **includes/** A folder containing recurring fragments of templates.


----------------------------
Documentation
----------------------------
To see the specific  `documentation`_.

.. _documentation: frontend/modules.html 
