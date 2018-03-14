
docker build . -t meerkat-docs

#cd 

export CURPATH=`pwd`/../

docker run -ti -v $CURPATH/meerkat_docs:/var/www/meerkat_docs \
       -v $CURPATH/meerkat_hermes:/var/www/meerkat_hermes\
       -v $CURPATH/meerkat_auth:/var/www/meerkat_auth\
       -v $CURPATH/meerkat_api:/var/www/meerkat_api\
       -v $CURPATH/meerkat_abacus:/var/www/meerkat_abacus\
       -v $CURPATH/meerkat_libs:/var/www/meerkat_libs\
       -v $CURPATH/meerkat_frontend:/var/www/meerkat_frontend\
       -v $CURPATH/meerkat_infrastructure:/var/www/meerkat_infrastructure\
       -v $CURPATH/meerkat_nest:/var/www/meerkat_nest\
       -v $CURPATH/meerkat_dev:/var/www/meerkat_dev\
       -v $CURPATH/meerkat_analysis:/var/www/meerkat_analysis\
       --env "MEERKAT_FRONTEND_SETTINGS=/var/www/meerkat_frontend/country_config/null_config.py" \
       --env "MEERKAT_NEST_DB_URL=postgresql+psycopg2://postgres:postgres@db/meerkat_db" \
       meerkat-docs bash
