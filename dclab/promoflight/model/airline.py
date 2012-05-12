from google.appengine.ext import db
import dclab

class Airline(db.Model):
    """Airline model"""
    name = db.StringProperty(required=True)

    @classmethod
    def add_airline(cls, airline_name):
        """Adds a new airline with with a uuid key automatically generated"""

        airline = cls(key_name=dclab.generate_uuid(), name=airline_name)
        return airline.put()

    @classmethod
    def update_airline(cls, unique_id, airline_name):
        a = cls.get_by_key_name(unique_id)

        if a is not None:
            a.name = airline_name
            return a.put()

        return None

    @classmethod
    def delete_airline(cls, unique_id, dependent=None):
        """
        Deletes an airline

        When dependent is passed, it should check if there are no dependents
        otherwise the deletion will not proceed.

        Does not run in a single transaction by design.
        Race condition/consistency is not an issue due to low deletion occurences.
        """

        result = False
        a = cls.get_by_key_name(unique_id)
        if a:
            if dependent is None:
                a.delete()
                if a.is_saved() == False:
                    result = True
            else:
                if dependent.has_airlines(unique_id) == False:
                    a.delete()
                    if a.is_saved() == False:
                        result = True
        return result

    @classmethod
    def get_airline(cls, unique_id):
        """Returns an airline from a given key"""
        return cls.get_by_key_name(unique_id)
    
    @classmethod
    def get_entity(cls, unique_id):
        """Alias to get_airline"""
        return cls.get_airline(unique_id)

    @classmethod
    def get_airlines(cls):
        """Returns all airlines sorted by name"""
        return cls.all().order('name')
