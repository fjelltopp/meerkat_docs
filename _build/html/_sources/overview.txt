===================
Overview
===================


The purpose of WHO-MEERKAT is to make data on epidemiological surveillance available in a useful way to varied group of stakeholders. We use cased based data submitted from mobile devices. The data is then aggregated, and presented to the user via websites and reports. The system is currently implemented in Jordan with over 300 clinics reporting.

All the data is submitted via ODK Collect to an ODK Aggregate Instance. From there the data is anonomised and passed on to the server running WHO-MEERKAT. Meerkat consits of three different parts meerkat_abacus for importing and aggregating data, meerkat_api gives an api for accessing aggregated data and meerkat_frontend which serves the data to the users


