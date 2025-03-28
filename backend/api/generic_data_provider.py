import os
import uuid

import json
# import mysql.connector


class GenericDataProvider:
    def __init__(self):
        db_config = os.getenv("SI_DB_CONFIG")
        if db_config is not None and db_config.startswith("mysql"):
            db_config_property = db_config.split(",")
            self.connection = mysql.connector.connect(
                    host= db_config_property[0],
                    user= db_config_property[1],
                    password= db_config_property[2],
                    database= db_config_property[3]
             )
            self.lookup_one_by_id = self.lookup_one_by_id_sql
            self.lookup_one_by_field = self.lookup_one_by_field_sql
            self.lookup_many_by_field = self.lookup_many_by_field_sql
            self.upsert_one = self.upsert_one_sql
        else:
            self.data = {}  # In-memory storage for JSON data

            self.use_predefined_json = False  # Flag to indicate if predefined JSON data should be used

            env_use_predefined_json = os.getenv("SI_SAVE_JSON")
            if env_use_predefined_json is not None and env_use_predefined_json.lower() == "true":
                self.use_predefined_json = True
                # Load predefined JSON data from a file if the file exists
                if os.path.exists("data.json"):
                    with open("data.json", "r") as f:
                        self.data = json.load(f)
    


            self.lookup_one_by_id = self.lookup_one_by_id_json
            self.lookup_one_by_field = self.lookup_one_by_field_json
            self.lookup_many_by_field = self.lookup_many_by_field_json
            self.upsert_one = self.upsert_one_json
             
             
    
    def lookup_one_by_id_sql(self, entity: str, id: str):
        """
        Fetch a single record from the specified entity (table) where the ID matches the given value.
        Returns the record as a dictionary of key-value pairs.
        """
        try:
            # Ensure the connection is established
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Database connection is not initialized.")

            # Create a cursor
            cursor = self.connection.cursor(dictionary=True)

            # Prepare and execute the query
            query = f"SELECT * FROM {entity} WHERE id = %s"
            cursor.execute(query, (id,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the cursor
            cursor.close()

            return result  # Returns None if no record is found
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None



        

    def lookup_one_by_field_sql(self, entity:str, field:str, value:str):
        """
        Fetch a single record from the specified entity (table) where the field matches the given value.
        Returns the record as a dictionary of key-value pairs.
        """
        try:
            # Ensure the connection is established
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Database connection is not initialized.")

            # Create a cursor
            cursor = self.connection.cursor(dictionary=True)

            # Prepare and execute the query
            query = f"SELECT * FROM {entity} WHERE {field} = %s"
            cursor.execute(query, (value,))

            # Fetch the result
            result = cursor.fetchone()

            # Close the cursor
            cursor.close()

            return result  # Returns None if no record is found
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def lookup_many_by_field_sql(self, entity: str, field: str, value: str):
        """
        Fetch multiple records from the specified entity (table) where the field matches the given value.
        Returns the records as a list of dictionaries.
        """
        try:
            # Ensure the connection is established
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Database connection is not initialized.")

            # Create a cursor
            cursor = self.connection.cursor(dictionary=True)

            # Prepare and execute the query
            query = f"SELECT * FROM {entity} WHERE {field} = %s"
            cursor.execute(query, (value,))

            # Fetch all results
            results = cursor.fetchall()

            # Close the cursor
            cursor.close()

            return results  # Returns an empty list if no records are found
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def upsert_one_sql(self, entity: str, id: str, data: dict):
        """
        Insert or update a record in the specified entity (table) based on the fields in the data dictionary.
        If a record with the given ID exists, it updates the record; otherwise, it inserts a new record.
        If the ID is None or an empty string, a new unique ID is generated.
        Returns the ID of the upserted record.
        """
        try:
            # Ensure the connection is established
            if not hasattr(self, 'connection') or self.connection is None:
                raise Exception("Database connection is not initialized.")

            # Generate a unique ID if the provided ID is None or empty
            if not id:
                id = str(uuid.uuid4())

            # Create a cursor
            cursor = self.connection.cursor()

            # Prepare column names and values for the query
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))
            update_clause = ", ".join([f"{key} = %s" for key in data.keys()])

            # Prepare the UPSERT query
            query = f"""
                INSERT INTO {entity} (id, {columns})
                VALUES (%s, {placeholders})
                ON DUPLICATE KEY UPDATE {update_clause}
            """

            # Combine values for INSERT and UPDATE
            values = (id, *data.values(), *data.values())

            # Execute the query
            cursor.execute(query, values)

            # Commit the transaction
            self.connection.commit()

            # Close the cursor
            cursor.close()

            return id  # Return the ID of the upserted record
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None


    def lookup_one_by_id_json(self, entity: str, id: str):
        """
        Fetch a single record from the in-memory JSON data where the ID matches the given value.
        Returns the record as a dictionary of key-value pairs.
        """
        if entity not in self.data:
            return None
        return self.data[entity].get(id)

    def lookup_one_by_field_json(self, entity: str, field: str, value: str):
        """
        Fetch a single record from the in-memory JSON data where the field matches the given value.
        Returns the record as a dictionary of key-value pairs.
        """
        if entity not in self.data:
            return None
        for record in self.data[entity].values():
            if record.get(field) == value:
                return record
        return None

    def lookup_many_by_field_json(self, entity: str, field: str, value: str):
        """
        Fetch multiple records from the in-memory JSON data where the field matches the given value.
        Returns the records as a list of dictionaries.
        """
        if entity not in self.data:
            return []
        return [record for record in self.data[entity].values() if record.get(field) == value]

    def upsert_one_json(self, entity: str, id: str, data: dict):
        """
        Insert or update a record in the in-memory JSON data based on the fields in the data dictionary.
        If the ID is None or an empty string, a new unique ID is generated.
        Returns the ID of the upserted record.
        """
        if entity not in self.data:
            self.data[entity] = {}

        # Generate a unique ID if the provided ID is None or empty
        if not id:
            id = str(uuid.uuid4())
        
        data["id"] = id

        # Insert or update the record
        self.data[entity][id] = data

        if self.use_predefined_json:
            # Save the updated data to the file
            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)

        return id

# create static version of GenericDataProvider
saved_data = GenericDataProvider()

# return static version of GenericDataProvider so it can be imported
def get_data_api() -> GenericDataProvider:
    return saved_data