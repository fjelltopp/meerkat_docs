===================
Meerkat Abacus
===================

The purpose of the abacus compenent of meerkat is to set up the database, import all data and then translate raw data into defined variables and aggregate the data.

------------------
Structure
------------------
config.py: generic and country specific config

model.py: specifies the database model

manage.py is a command-line tool to set-up the database and import data. Usage as follows: 

.. argparse::
   :module: meerkat_abacus.manage
   :func: parser
   :prog: manage.py

taske_queue.py: implements taske queue for adding new data and aggregating new data

database_util: various utility functions used 

aggregate: helper scripts for aggregation

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

For each variable we can also have a secondary condition which requires that a specified column has a specified value.
