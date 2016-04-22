==================
Meerkat API
==================

Meerkat API gives access to the data proccessed by meerkat abacus. It is build using flask and communicates with the same DB as abacus.

Most of the API needs an api_key for authentication. The api_key is set in the config file. 

-------------------
API documentation
-------------------
.. autoflask:: meerkat_api:app
   :undoc-static:
