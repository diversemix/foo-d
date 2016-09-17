#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module to populate redis from the CSV files.
"""
import logging
import csv
import time
from decimal import Decimal

class GeoCache(object):
    __error_fmt = "{} : Incorrect number of row items!"
    __prefix = 'postcode:'
    __locations = 'locations'

    def __init__(self, config):
        """ Use a json object as the config item (dependency injection)
        """
        if 'csv_files' not in config:
            raise ValueError("Could not find configuration")

        _config = config['csv_files']

        if 'postcodes' not in _config:
            raise ValueError("No postcode file in config.")
        else:
            self.__postcodes = _config['postcodes']

        if 'pubs' not in _config:
            raise ValueError("No pubs file in config.")
        else:
            self.__pubs = _config['pubs']

        self.__num_postcodes = 0
        self.__num_pubs = 0

    @classmethod
    def clean_postcode(cls, postcode):
        """ Strips whitespace and removes any spaces from the string."""
        return postcode.strip().replace(' ','')

    @classmethod
    def get_postcode(cls, code):
        """ Cleans up and adds the prefix."""
        return cls.__prefix + GeoCache.clean_postcode(code)

    def populate(self, redis_client):
        logging.info("Populating cache with postcodes")
        with open(self.__postcodes, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                # Validate the row
                if len(row) != 5:
                    raise ValueError(self.__error_fmt.format(self.__postcodes))
                code = GeoCache.get_postcode(row[0])
                # Now add this postcode
                redis_client.geoadd( self.__locations,
                                     Decimal(row[3]),
                                     Decimal(row[4]),
                                     code)
                self.__num_postcodes += 1

        logging.info("Finished reading %d postcodes", self.__num_postcodes)
        logging.info("Populating cache with pubs")

        with open(self.__pubs, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) != 2:
                    raise ValueError(self.__error_fmt.format(self.__pubs))

                postcode = GeoCache.get_postcode(row[1])
                name = row[0].strip()

                # Look up postcode location
                locations = redis_client.geopos(self.__locations, postcode)
                if locations and len(locations):
                    # Grab the first location
                    _lat, _long = locations[0]
                    # Now add this pub
                    redis_client.geoadd(self.__locations, _lat, _long, name)
                    self.__num_pubs += 1
                else:
                    logging.error("*** SKIPPING *** Could not find position for: %s", postcode)

        logging.info("Finished reading %d pubs", self.__num_pubs)

    def get_pubs_here(self, redis_client, postcode, radius):
        """Main function to get the pubs in a given radius.
        Returns a tuple: first item is the list of pubs, second is the time
        taken in ms.
        """
        time_start = time.time()

        code = GeoCache.get_postcode(postcode)
        found = redis_client.georadiusbymember(self.__locations, code,
                    radius, withdist=True, unit='m', sort='ASC')

        # filter out the postcode centres
        pubs = [ loc for loc in found if not loc[0].startswith(self.__prefix) ]

        time_end = time.time()
        return pubs, (time_end - time_start) * 1000.0


if __name__ == '__main__':
    import redis

    print(redis.VERSION, redis.__file__)

    _pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    _redis_client = redis.Redis(connection_pool=_pool)

    # The entry point in this module will test the class...
    _cache = GeoCache({ 'csv_files' : {
                                'postcodes' : 'data/postcodes.csv',
                                'pubs' : 'data/pubnames.csv'
                                }
    })

    _cache.populate(_redis_client)
    print(_cache.get_pubs_here(_redis_client, "KT109AX", "100000"))
    print(_cache.get_pubs_here(_redis_client, 'SO46BG', "10000"))
