===================
Meerkat Abacus
===================

The purpose of the abacus component of Meerkat is to set up the database, import all data and then translate raw data into defined variables in the data table.

Abacus uses a PostgreSQL database and uses celery as a task manager. When celery starts the database is setup, and then new data is added every hour. 

Abacus is easily configurable to run for different implementations (or countries). The country specific configuration is detailed below.

------------------
Structure
------------------
config.py: application configuration

model.py: specifies the database model

manage.py is a command-line tool to set-up the database and import data. Usage as follows: 

.. argparse::
   :module: meerkat_abacus.manage
   :func: parser
   :prog: manage.py

data_management.py: implements all the database functionality

task_queue.py: implements task queue for adding new data and aggregating new data

util: various utility functions used 

codes: scripts for turning data into codes

country_config: configuration files for a specific country

----------------
Data Flow
----------------
When celery is stared in meerkat_abacus, we start by setting up the database. Then we import the data before transforming it into structured data ready for use. To accomplish this we do the following steps:

1. Create database and setup all tables according to the model.py file.
2. Import location data.
    We import regions, districts and clinics from location files specified in the config directory. Each clinic can have multiple tablets associated with it.
3. Import variables and links.
   We import variables from the codes file and links from the link file.
4. Download data from S3 or create new *fake* data.
   This data consists of csv-files, one for each from. We always have three forms, a case report, a daily register and alert investigations forms. We can add more forms in the config file. 
5. Import data in to db.
   We import all the data from the csv-files into the db, making sure only data from approved tablets are imported. We store all the form data by rows in a JSONB database column. This means that we make no assumptions about what fields exists or how the data is structured. We can also define quality controls on the data to remove wrong data. These quality controls are implemented in the codes file. 
6. We translate raw data into structured data. The structured data has on out of three types. Case, Visit or Register. A Case is record that spans the whole history of a patient for one disease. So a patient could have two cases if the system registered them with two different diseases. A visit is one visit to the clinic, either a new visit or a return visit. A register is for aggregated data entry, mainly used for the daily registers.
6.1 We go through each data type in the data_types.csv file to determine which rows in the raw data correspond to this data type. We then find all the linked rows to this data row.
6.2  The variables we have imported tells us how to translate raw data from the forms into structured data. E.g the variables for gender tells us what field in the raw_data should be treated as gender. After this translation one should not need to know any details about the structure of the raw data. This step is the most time-consuming and some effort has been spent to optimise the speed. Indivdual alerts are added at this stage.
7. We determine threshold based alerts. 
9. The data is ready for use by the API and frontend. 



---------------
Variables
---------------

The main abstraction in meerkat_abacus is that we translate raw data from forms by specifically defined codes or variables. After the raw data from the form has been mapped to the correct variables one should not need to know anything about the form structure any more.

The codes are specified in a codes.csv file, e.g country_config/demo_codes.csv. Abacus currently supports the following codes:

* match: The value has to match exactly any of the conditions
* sub_match: A substring of the value has to match any of the conditions
* between: We calculate a value that has to be between the two condtions.
* calc: We calcaulate a value and return that
* value: We return the value

This basic types can be compined with "and" and "or". 

* Gender: gender
* Nationality: nationality
* Status: status
* Age: age
* Presenting Complaint: pc
* Vaccination: epi
* Smoking: public
* Modules: module
* Pregnancy: pregnancy
* Icd Chapters: Chapter
* Icd Blocks: Name of Chapter it belongs to
* Icd Disease: Name of Block it belongs to
* Cd tab(also alert names): cd_tab
* NCD tab: ncd_tab
* Mental Health: mhgap
* Child Health: imci
* Which Block are included as Child disease: for_child
* ICD block into disease type: cd, ncd, mh, injury, child,rh other

--------------------
Configuration
--------------------

It is necessary to provide configuration for meerkat abacus to work.

The config.py file has the application level configuration and also imports the country specific configs. Many of the application level configuration variables can be overwritten by environmental variables:

* MEERKAT_ABACUS_DB_URL: db_url
* DATA_DIRECTORY: path to directory where we store data csv files
* COUNTRY_CONFIG_DIR: path to directory with country config
* COUNTRY_CONFIG: name of country config file
* NEW_FAKE_DATA: if we should generate fake data
* GET_DATA_FROM_S3: if we should download data from an S3 bucket
* START_CELERY: if we want to star the celery hourly tasks

The country level configuration needs the following information:

Main config file: 
--------------------
s3_bucket: the url to the s3 bucket if one is used

country_config dictionary: this dictionary includes almost all the information about the country such as:

* name: name
* tables: name of the forms/db tables we are using
* codes_file: name of codes file
* links_file: name of file with link defs
* country_tests: name of files that implements some country specific testing
* epi_week: how epi_weeks are calculated, international gives the start of epi week 1 at 01/01. day:week_day gives the start on the first week_day(Mon=0) after 01/01
* locations: specifies the csv files with location data for the region, district and clinic level
* form_dates: which field in the form gives the date of the form
* fake_data:  how to generate fake data for the form
* alert_data: what data from the case reports to include in alerts
* alert_id_length: the number of characters from the uuid to take as the alert id

  
Locations
-----------

We have three levels of locations: Regions, Districts and Clinics.

Each level needs a different csv file with locations. For clinics, each record is one tablet with a specific deviceid. Tablets with the same clinic name in the same district will be merged into one clinic.

Codes
------
A codes file is needed to specify how to translate the raw data into useful data. See variables for details on naming conventions
 

----------------------------
Documentation
----------------------------
To see the specific  `documentation`_.

.. _documentation: abacus/modules.html 
