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
   We import all the data from the csv-files into the db, making sure only data from approved tablets are imported. We store all the form data by rows in a JSONB database column. This means that we make no assumptions about what fields exists or how the data is structured.
6. We translate raw data into structured data.
   The variables we have imported tells us how to translate raw data from the forms into structured data. E.g the variables for gender tells us what field in the raw_data should be treated as gender. After this translation one should not need to know any details about the structure of the raw data. This step is the most time-consuming and some effort has been spent to optimise the speed.
7. Add alerts and send alert notifications
   Certain codes for some important communicable diseases should trigger alerts. Alerts are stored in a separate table and needs to be investigated on the ground. By using meerkat_heremes we sent emails and sms notifications for alerts. 
8. We add link
   We need to add links between data in different (or potentially the same) tables. For example we want to link alerts to alert investigations.
9. The data is ready for use by the API and frontend. 



---------------
Variables
---------------

The main abstraction in meerkat_abacus is that we translate raw data from forms by specifically defined codes or variables. After the raw data from the form has been mapped to the correct variables one should not need to know anything about the form structure any more.

The codes are specified in a codes.csv file, e.g country_config/demo_codes.csv. Abacus currently supports the following codes:

* count - Counts all rows with non-zero entry in the specified field of the form
* count_occurrence - Counts rows where condition appears in field
* count_occurrence_in - Counts rows where condition is a sub string of the value in the field
* int_between - An integer between the two numbers specified in condition
* count_occurrence_int_between - must both full fill a count_occurrence and a int_between on two different columns
* count_occurrence_in_int_between - must both full fill a count_occurrence_in and a int_between on two different columns
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

We have the following category names:


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
  
Links
------

Links implement links between two tables in the database. This could for example be Alert Investigations linking alerts to alert_investigations. Links are defined in the country_config/demo_links.py file.

A link definition looks like this::

      {
        "id": "alert_investigation",
        "name": "Alert Investigation",
        "from_table": "Alerts",
        "from_column": "id",
        "from_date": "date",
        "to_table": "alert",
        "to_column": "pt./alert_id",
        "to_date": "end",
        "which": "last",
        "data": {
            "status": {
                "Ongoing": {"column": "alert_labs./return_lab",
                            "condition": ["", "unsure"]},
                "Confirmed": {"column": "alert_labs./return_lab",
                              "condition": "yes"},
                "Disregarded": {"column": "alert_labs./return_lab",
                                "condition": "no"}
            },
            "checklist": {
                "Referral": {"column": "pt./checklist",
                             "condition": "referral"},
                "Case Managment": {"column": "pt./checklist",
                                   "condition": "case_management"},
                "Contact Tracing": {"column": "pt./checklist",
                                    "condition": "contact_tracing"},
                "Laboratory Diagnosis": {"column": "pt./checklist",
                                         "condition": "return_lab"},
            },
            "investigator": {
                "investigator": {"column": "deviceid",
                                 "condition": "get_value"
                                 }
                }
        }

    }
We have a *from* table linked to a *to* table linked on the same value in *from_column* and *to_column*. The data structure defines what data from the *to* table we store with the link. The *which* key determines how we deal with multiple *to* records linking to one *from*. With *last* we take the latest *to* row that matches. 

----------------------------
Documentation
----------------------------
To see the specific  `documentation`_.

.. _documentation: abacus/modules.html 
