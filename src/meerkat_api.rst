==================
Meerkat API
==================
Meerkat API gives access to the data proccessed by meerkat abacus. It is build using flask and communicates with DB setup by Abacus. The main functionality is to aggregate data over time and location and give access to all the variables and locations in the DB. The API provides all the data for Meerkat Frontend and could be accessed by other applications. To access most methods an api-key is required. The api-key is set in the config. 

We use flaskRESTful to create the API and flask-sqlalcemy to access the db

---------------
Structure
---------------

__init__.py: sets up the flask app and all the urls

authentication.py: Methods for authtication

util/__init__.py: Various utility methods

resources/: Folder containing the following files: 

* locations.py: Location information including a location tree
* variables.py: Access to all the variables used in Abacus
* data.py: Aggregated data over time and locations
* alerts.py: Access to alerts and alert_investigations
* epi_week.py: Calculating epi weeks
* explore.py: Export various data as csv-files
* export_data.py: Gives options to look at cross tables and timelines of data
* map.py: Mapping different data
* reports.py: Data for specified reports
* completeness.py: Calculating completeness of reporting
* links.py: Retrive link information
* frontpage.py: High level information that can be access without an api_key
  
----------
Config
----------
The API key needs to specified in a file pointed to by the environmental variable MEERKAT_API_SETTINGS. We use a random uuid as the api-key. This api-key will give access to all of the api. 

-------------------
API urls
-------------------
.. autoflask:: meerkat_api:app
   :undoc-static:

------------------
Utility Functions
------------------
.. automodule:: meerkat_api.util
   :members:

---------------------------
Report Helper Functions
---------------------------
.. automodule:: meerkat_api.resources.reports
   :members: fix_dates, get_disease_types, make_dict, top, get_variable_id, get_variables_category, disease_breakdown, get_latest_category, refugee_disease
