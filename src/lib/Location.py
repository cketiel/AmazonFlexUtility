import json
import os

class Location:
        
    def __init__(self, id=None, name=None, state="current"):
        self.id = id
        self.name = name
        self.state = state

    @classmethod
    def updateList(cls, location_list):
        file_path = os.path.join("data", "location.all.json")
        with open(file_path, "w") as json_file:
            json.dump([vars(location) for location in location_list], json_file)
        desiredWarehouses = []
        for loc in location_list:
            if loc.state == "current":
                desiredWarehouses.append(str(loc.id))
        with open("config.json", "r+") as configFile:
            config = json.load(configFile)
            config["desiredWarehouses"] = desiredWarehouses
            configFile.seek(0)
            json.dump(config, configFile, indent=2)
            configFile.truncate()

    @classmethod
    def getAll(cls):
        file_path = os.path.join("data", "location.all.json")
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return [cls(**location) for location in data]
    
    @classmethod
    def get(cls, target_id):
        locations = cls.getAll()
        for location in locations:
            if location.id == target_id:
                return location
        return None  # Si no se encuentra ninguna ubicación con el ID especificado


    @classmethod
    def addLocation(cls, new_location):
        locations = cls.getAll()
        for location in locations:
            if location.id == new_location.id:
                location.state = "current"
                cls.updateList(locations)
                return
        locations.append(new_location)
        cls.updateList(locations)

    @classmethod
    def removeLocation(cls, location_to_remove):
        locations = cls.getAll()
        for location in locations:
            if location.id == location_to_remove.id:
                location.state = "rest"
                cls.updateList(locations)
                return

    @classmethod
    def getCurrentLocations(cls):
        locations = cls.getAll()
        return [location for location in locations if location.state == "current"]

    @classmethod
    def getRestLocations(cls):
        locations = cls.getAll()
        return [location for location in locations if location.state == "rest"]

    @classmethod
    def addLocationInit(cls, id, name):
        file_path = os.path.join("data", "location.all.json")

        # Verificar si el archivo JSON existe
        # Check if the JSON file exists
        if not os.path.exists(file_path):
            # Si no existe, crear el archivo y agregar el objeto inicial
            # If it does not exist, create the file and add the initial object
            initial_location = cls(id, name, "rest")
            with open(file_path, "w") as json_file:
                json.dump([vars(initial_location)], json_file)
        else:
            # Si el archivo ya existe, obtener su contenido y agregar el objeto inicial
            # If the file already exists, get its contents and add the initial object
            locations = cls.getAll()
            new_location = cls(id, name, "rest")
            locations.append(new_location)
            cls.updateList(locations)

if __name__ == "__main__":
    # Ejemplo de uso
    # Example of use
    Location.addLocationInit(3, "Lugar C")

    # Obtener todas las ubicaciones
    # Get all locations
    all_locations = Location.getAll()
    for location in all_locations:
        print(f"ID: {location.id}, Name: {location.name}, State: {location.state}")
