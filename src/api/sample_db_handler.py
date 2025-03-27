
class SavedData:
    def __init__(self):
        self.data = {}
    
    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

# create static version of SavedData
saved_data = SavedData()

# return static version of SavedData so it can be imported
def get_saved_data_api() -> SavedData:
    return saved_data