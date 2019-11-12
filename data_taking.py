from datetime import datetime


class BikeTimes():
    def __init__(self):
        self.date = datetime.now()
        self.hour = self.date.hour
        self.minute = self.date.minute
        self.url = 'https://api.tfl.gov.uk/Place/Type/BikePoint'
        self.data = requests.get(self.url).json()
        
    def save_data(self):
        with open(f'./bike_data_{self.hour}_{self.minute}.json', 'w+') as f:
            f.write(json.dumps(self.data, sort_keys = True, indent = 4))
        
        