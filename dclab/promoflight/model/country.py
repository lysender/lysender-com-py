from google.appengine.ext import db
import dclab

class Country(db.Model):
    """Country model"""
    name = db.StringProperty(required=True)

    @classmethod
    def add_country(cls, country_name):
        """Adds a new country with with a uuid key generated on the fly"""
        c = cls(key_name=dclab.generate_uuid(), name=country_name)
        return c.put()

    @classmethod
    def update_country(cls, unique_id, country_name):
        """Updates country info"""
        c = cls.get_by_key_name(unique_id)

        if c is not None:
            c.name = country_name
            return c.put()

        return None

    @classmethod
    def delete_country(cls, unique_id, dependent=None):
        """Deletes country"""
        c = cls.get_by_key_name(unique_id)
        result = False

        if c is not None:
            if dependent is None:
                c.delete()
                if c.is_saved() == False:
                    result = True
            else:
                if dependent.has_countries(unique_id) == False:
                    c.delete()
                    if c.is_saved() == False:
                        result = True

        return result

    @classmethod
    def get_country(cls, unique_id):
        """Returns a country from a given key"""
        return cls.get_by_key_name(unique_id)

    @classmethod
    def get_entity(cls, unique_id):
        """Alias to get_country"""
        return cls.get_country(unique_id)
    
    @classmethod
    def get_countries(cls, ):
        """Returns all countrys sorted by name"""
        return cls.all().order('name')