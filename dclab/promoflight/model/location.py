from google.appengine.ext import db
import dclab

class Location(db.Model):
    """Location model"""
    name = db.StringProperty(required=True)

    @classmethod
    def add_location(cls, location_name):
        """Adds a new location with with a uuid key generated on the fly"""
        loc = cls(key_name=dclab.generate_uuid(), name=location_name)
        return loc.put()

    @classmethod
    def update_location(cls, unique_id, location_name):
        """Updates location info"""
        loc = cls.get_by_key_name(unique_id)

        if loc is not None:
            loc.name = location_name
            return loc.put()

        return None

    @classmethod
    def delete_location(cls, unique_id, dependent=None):
        """Deletes location"""
        loc = cls.get_by_key_name(unique_id)
        result = False

        if loc is not None:
            if dependent is None:
                loc.delete()
                if loc.is_saved() == False:
                    result = True
            else:
                if dependent.has_locations(unique_id) == False:
                    loc.delete()
                    if loc.is_saved() == False:
                        result = True

        return result

    @classmethod
    def get_location(cls, unique_id):
        """Returns a location from a given key"""
        return cls.get_by_key_name(unique_id)

    @classmethod
    def get_entity(cls, unique_id):
        """Alias to get_location"""
        return cls.get_location(unique_id)
    
    @classmethod
    def get_locations(cls, ):
        """Returns all locations sorted by name"""
        return cls.all().order('name')