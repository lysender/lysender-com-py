from google.appengine.ext import db

import dclab
from dclab.promoflight.model.airline import Airline
from dclab.promoflight.model.location import Location

class Promo(db.Model):
    """Promo model

    Each promo belongs to an airline
    Each promo has origin and destination locations
    """

    title = db.StringProperty(required=True)
    airline = db.ReferenceProperty(Airline,
                                   required=True,
                                   collection_name='promos')

    origin = db.ReferenceProperty(Location,
                                  required=True,
                                  collection_name='origin_promos')

    destination = db.ReferenceProperty(Location,
                                       required=True,
                                       collection_name='destination_promos')

    selling_period_start = db.DateProperty(required=True)
    selling_period_end = db.DateProperty(required=True)
    travel_period_start = db.DateProperty(required=True)
    travel_period_end = db.DateProperty(required=True)
    description = db.StringProperty(required=True, indexed=False)
    add_date = db.DateTimeProperty(auto_now_add=True)
    modified_date = db.DateTimeProperty(auto_now=True)

    @classmethod
    def add_promo(cls, data):
        """
        Adds a promo with airline and origin/destination information

        airline, origin and destination must be db.Key

        Data keys are the following:
            title
            airline
            origin
            destination
            selling_period_start
            selling_period_end
            travel_period_start
            travel_period_end
            description

        Add date and modified date is automatically set
        """

        if isinstance(data['airline'], db.Key) and isinstance(data['origin'], db.Key) and isinstance(data['destination'], db.Key):
            p = Promo(key_name=dclab.generate_uuid(),
                      title=data['title'],
                      airline=data['airline'],
                      origin=data['origin'],
                      destination=data['destination'],
                      selling_period_start=data['selling_period_start'],
                      selling_period_end=data['selling_period_end'],
                      travel_period_start=data['travel_period_start'],
                      travel_period_end=data['travel_period_end'],
                      description=data['description'])

            return p.put()
        return None

    @classmethod
    def get_promo(cls, unique_id):
        """Returns a promo based on promo key"""
        return cls.get_by_key_name(unique_id)

    @classmethod
    def update_promo(cls, unique_id, data):
        """
        Updates a promo with airline and origin/destination information

        Data keys are the following:
            title
            airline
            origin
            destination
            selling_period_start
            selling_period_end
            travel_period_start
            travel_period_end
            description

        Modified date is automatically set
        """
        p = cls.get_by_key_name(unique_id)
        if p is None:
            return None

        entity_keys = ['airline', 'origin', 'destination']
        for ek in entity_keys:
            if ek in data:
                if not isinstance(data[ek], db.Key):
                    return None

        for k, v in data.iteritems():
            setattr(p, k, v)

        return p.save()

    @classmethod
    def delete_promo(cls, unique_id):
        """Deletes promo"""
        p = cls.get_by_key_name(unique_id)

        if p is not None:
            p.delete()
            if p.is_saved() == False:
                return True

        return False

    @classmethod
    def get_promo_list_query(cls, limit, params):
        """
        Returns a dict {query, query_key_list} for promo lists based on filters and sorting

        limit       Maximum promos returned

        Keyword arguments:

        query           Models query object, used to inject query object
        keys_only       True or False, only works when query is not injected
        airline         Airline key, filter for airlines, None by default
        origin          Origin key, filter for origin locations, None by default
        destination     Destination key, filter for destination locations, None by default
        add_date_sort   None by default, values are ASC,DESC or None
        selling_period_start_sort     None by default, values are ASC,DESC or None
        travel_period_start_sort      None by default, values are ASC,DESC or None
        """
        query = None
        query_key = ['limit=' + str(limit)]

        # Query object injection
        if 'query' in params:
            query = params['query']
        else:
            keys_only_flag = False
            if 'keys_only' in params and params['keys_only'] == True:
                query_key.append('keys_only=True')
                keys_only_flag = True

            query = cls.all(keys_only=keys_only_flag)

        # Check for entity key filters
        keys = ['airline', 'origin', 'destination']
        for k in keys:
            if k in params:
                query.filter('%s = ' % k, params[k])
                query_key.append('%s=%s' % (k, params[k]))

        # Check for date sorting
        dates = ['add_date', 'selling_period_start', 'travel_period_start']
        sorts = ['ASC', 'DESC']

        for f in dates:
            fsort = f + '_sort'
            if fsort in params and params[fsort] in sorts:
                if params[fsort] == 'ASC':
                    query.order(f)
                    query_key.append('%s=%s' % (fsort, 'ASC'))
                else:
                    query.order('-' + f)
                    query_key.append('%s=%s' % (fsort, 'DESC'))

        return {'query': query, 'query_key': ','.join(query_key)}

    @classmethod
    def get_promo_list(cls, limit, params={}):
        """
        Returns a list of promo based on filters, sorting and cursor

        limit       Maximum promos returned

        Param arguments:

        start_cursor    The cursor to use for fetching result, None by default
        airline         Filter for airlines, None by default
        origin          Filter for origin locations, None by default
        destination     Filter for destination locations, None by default
        add_date_sort   DESC by default, values are ASC,DESC
        selling_date_start_sort     None by default, values are ASC,DESC or None
        travel_date_start_sort      None by default, values are ASC,DESC or None
        """
        gquery = cls.get_promo_list_query(limit, params)

        if len(gquery) != 2:
            return None

        query = gquery['query']

        if 'start_cursor' in params:
            query.with_cursor(params['start_cursor'])

        return query.fetch(limit)

    @classmethod
    def get_promo_cursors(cls, per_page, limit, params={}):
        """
        Returns a list of {promo_cursors, has_more} based on filters, sorting and cursor
        has_more means that there are more data beyond the limit specified (True/False)

        Take note that the cursor list is always 1 page ahead of the list. Meaning that
        the first cursor entry is actually for the second page and not for the first page.
        Therefore, the cursors returned is actually more than requested. 

        The excess cursors are indicators that there are more data forward the cursor. 
        The first page number of the pagination list (cursors) is either no cursor or
        the start_cursor.

        per_page    Maximum promos per page
        limit       Maximum cursors returned

        Params argument:

        start_cursor    The cursor to use for fetching result, None by default
        airline_id      Filter for airlines, None by default
        origin_id       Filter for origin locations, None by default
        destination_id  Filter for destination locations, None by default
        add_date_sort   DESC by default, values are ASC,DESC
        selling_date_start_sort     None by default, values are ASC,DESC or None
        travel_date_start_sort      None by default, values are ASC,DESC or None
        """
        params['keys_only'] = True
        gquery = cls.get_promo_list_query(limit, params)

        query = gquery['query']

        if 'start_cursor' in params:
            query.with_cursor(params['start_cursor'])

        cursors = []

        for i in range(limit):
            result = query.fetch(per_page)
            if result:
                new_cursor = query.cursor()
                cursors.append(new_cursor)
                query.with_cursor(new_cursor)
            else:
                break

        return cursors

    @classmethod
    def get_latest_promos(cls, limit=10):
        """Returns latest promos"""
        result = cls.get_promo_list(limit, {'add_date_sort': 'DESC'})

        if result and isinstance(result, list) and len(result) > 0:
            return result

        return None

    @classmethod
    def has_airlines(cls, airline_id):
        """Returns True when the specified airline is associated with any promo"""
        k = db.Key.from_path('Airline', airline_id)
        q = cls.all(keys_only=True)
        q.filter('airline_id = ', k)

        if q.get() is not None:
            return True

        return False

    @classmethod
    def has_locations(cls, location_id):
        """Returns True when the specified location is associated with any promo"""
        k = db.Key.from_path('Location', location_id)
        origin = cls.all(keys_only=True)
        origin.filter('origin = ', k)

        if origin.get() is not None:
            return True

        dest = cls.all(keys_only=True)
        dest.filter('destination = ', k)

        if dest.get() is not None:
            return True

        return False
