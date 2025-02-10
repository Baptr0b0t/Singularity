class Gameobjectmanager:

    #make multiple scene
    alive_objects = []

    @classmethod
    def add_object(cls, game_object):
        cls.alive_objects.append(game_object)

    @classmethod
    def remove_object(cls, game_object):
        if game_object in cls.alive_objects:
            cls.alive_objects.remove(game_object)

    @classmethod
    def find_by_tag(cls, tag):
        return [obj for obj in cls.alive_objects if obj.has_tag(tag)]

    @classmethod
    def get_all_alive(cls):
        return cls.alive_objects

    #add gameobject scene updater
