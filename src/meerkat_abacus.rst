===================
Meerkat Abacus
===================

The purpose of the abacus compenent of meerkat is to set up the database, import all data and then translate raw data into defined variables in the data table.

Abacus uses a postgresql database and runs on celery. When celery starts the database is setup and then new data is added every hour. Celery depends on rabbitMQ. Abacus uses sqlalchemy for all comunication with the database.

Abacus is easily configurable to run for different implementations(or countries). The country specfic configuration is detail bellow.

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

data_managment.py: implements all the database functionality

taske_queue.py: implements taske queue for adding new data and aggregating new data

util: various utility functions used 

codes: scripts for turning data into codes

country_config: configuration files for a specfic country

---------------
Variables
---------------

The main abstraction in meerkat_abacus is that we translate raw data from forms by specifically defined codes or variables. After the raw data from the form has been mapped to the correct variables one should not need to know anything about the form sturcutre any more.

The codes are specified in a codes.csv file, e.g data/demo_codes.csv. Abacus currently supports the following codes:

* count - Counts all rows with non-zero entry in the specified field of the form
* count_occurence - Counts rows where condtion appears in field
* count_occurence_in - Counts rows where condition is a substring of the value in the field
* int_between - An integer between the two numbers specified in condition
* count_occurence_int_between - must both fullfill a count_occurence and a int_between on two different columns
* count_occurence_in_int_between - must both fullfill a count_occurence_in and a int_between on two different columns
* sum - Returns the numerical value of the field
* not_null - true for non-null values of the field
   
* calc_between - allows you to specify a mathematical expression of multiple columns in the row. The calculated value should then be between the given boundaries

For each variable we can also have a secondary condition which requires that a specified column has a specified value.

It is then important that once a code has been given an ID it should not change. If two countries have the same code, the codes should have the same id.

We use the following codes:

* Total: tot_1
* Gender: gen_n
* Nationality: nat_n
* Age(including the gender age breakdown): age_n
* Status: sta_n
* Cd tab: cmd_n
* Ncd tab: ncd_n
* ICD Chapters: icc_n
* ICD Blocks: icb_n
* Mhgap: mhg_n
* IMCI: imc_n
* Vaccination: vac_n
* Smoking: smo_1
* Modules: mod_n
* Visit type: vis_n
* Pregnancy: pre_n
* From Daily Register: reg_n
* Individual icd codes: icd_n

  The following category names:


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
* ICD block into diease type: cd, ncd, mh, injury, child,rh other

--------------------
Configuration
--------------------

It is nescessary to provide configuration for meerkat abacus to work.

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
* alert_id_length: the number of characters from the uuid to take aas the alert id

  
Locations
-----------

We have three levels of locations: Regions, Districts and Clinics.

Each level needs a different csv file with locations. For clinics, each record is one tablet with a specific deviceid. Tablets with the same clinic name in the same district will be merged into one clinic.

Codes
------
A codes file is needed to specify how to translate the raw data into useful data. See variables for details on naming conventions
  
Links
------

Links implement links between two tables in the database. This could be alert investigations. 

----------------------------
Documentation
----------------------------
To see the specific  `documentation`_.

.. _documentation: abacus/modules.html 
