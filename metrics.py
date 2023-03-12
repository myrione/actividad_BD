import datetime
import requests
import statistics
from config import cfg_item

class Metrics:
    
    """
    La clase Metrics extrae y procesa información de diversas APIs para implementarla en los distintos comandos empleados en el bot.
    """
    
    def __init__(self):
        
        self.__today, self.__yesterday, self.__timestamp_now, self.__timestamp_start_week, self.__timestamp_start_month, self.__last_week, self.__last_month = self.get_dates()
        self.__data = self.get_FG_data()
        self.__weekly_avg, self.__monthly_avg = self.get_FG_average_values()
        self.history = self.FG_history()
        self.SOPR = self.SOPR()
        self.market_data = self.market_info()
        self.active_addresses = self.ative_addresses()
        self.hash_rate, self.avg_week_difficulty = self.mining()
                       
    def get_dates(self):
        
        now = datetime.datetime.now()
        timestamp_now = now.timestamp()
        start_week = now - datetime.timedelta(days=6)
        start_month = now - datetime.timedelta(days=29)
        timestamp_start_week = start_week.timestamp()
        timestamp_start_month = start_month.timestamp()
        today = now.strftime("%d-%m-%Y")
        yesterday = (now - datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        last_week = [(now - datetime.timedelta(days=i)).strftime('%d-%m-%Y') for i in range(1, 8)]
        last_month = [(now - datetime.timedelta(days=i)).strftime('%d-%m-%Y') for i in range(1, 33)]
    
        return today, yesterday, timestamp_now, timestamp_start_week, timestamp_start_month, last_week, last_month
        
    def get_FG_average_values(self):
        
        weekly_values = []
        monthly_values = []
       
        for entry in self.__data['data']:
            if entry['timestamp'] in self.__last_week:
                weekly_values.append(int(entry['value']))
        
        for entry in self.__data['data']:
            if entry['timestamp'] in self.__last_month:
                monthly_values.append(int(entry['value']))

        weekly_average = int(statistics.mean(weekly_values))
        monthly_average = int(statistics.mean(monthly_values))
        
        return weekly_average, monthly_average
        
    def get_FG_data(self):
        
        endpoint = "https://api.alternative.me/fng/?limit=30&format=json&date_format=world"
        response = requests.get(endpoint)
        data = response.json()
        return data
    
    def get_emotion(self, param):
        ranges = {'Miedo extremo' : range(0,31), 'Miedo': range(31, 46), 'Neutral': range(46, 56), 'Avaricia': range(56, 76), 'Avaricia extrema': range(76,101)}
        
        for key, value in ranges.items():
            if int(param) in value:
                return key
 
    def FG_history(self):
      
        history = []

        for entry in self.__data['data']:
            if entry['timestamp'] == self.__today:
                value = int(entry['value'])
                history.append(f"{value}  {self.get_emotion(value)}")

            elif entry['timestamp'] == self.__yesterday:
                value = int(entry['value'])
                history.append(f"{value}  {self.get_emotion(value)}")
        
        history.append(f"{self.__weekly_avg} {self.get_emotion(self.__weekly_avg)}")
        history.append(f"{self.__monthly_avg} {self.get_emotion(self.__monthly_avg)}")
       
        return history
    
    def SOPR(self):
        
        params = {
        'a': 'BTC', 
        'api_key': cfg_item("Glassnode", "token"),
        's' : int(self.__timestamp_start_week),
        'u' : int(self.__timestamp_now)
        }
        endpoint = 'indicators/sopr'
        
        res = requests.get(cfg_item("Glassnode", "base_url") + endpoint, params=params)
        SOPR_data = res.json()
        SOPR_index_list = [entry['v'] for entry in SOPR_data]        
        return SOPR_index_list
    
    def ative_addresses(self):
        
        params = {
        'a': 'BTC', 
        'api_key': cfg_item("Glassnode", "token"),
        's' : int(self.__timestamp_start_month),
        'u' : int(self.__timestamp_now)
        }
        endpoint = 'addresses/active_count'
        
        res = requests.get(cfg_item("Glassnode", "base_url") + endpoint, params=params)
        adresses_monthly = [entry['v'] for entry in res.json()]
        weekly_growth  = adresses_monthly[0] - adresses_monthly[6]
        monthly_growth  = adresses_monthly[0] - adresses_monthly[-1]
        
        return weekly_growth, monthly_growth

    def mining(self):
        
        params = {
        'a': 'BTC', 
        'api_key': cfg_item("Glassnode", "token"),
        's' : int(self.__timestamp_start_week),
        'u' : int(self.__timestamp_now)
        }
        endpoint_hash = 'mining/hash_rate_mean'
        endpoint_difficulty = 'mining/difficulty_latest'
        
        res_hash = requests.get(cfg_item("Glassnode", "base_url") + endpoint_hash, params=params)
        hash_data = res_hash.json()
        hash_rate = [entry['v'] for entry in hash_data]
        avg_week_hash_rate = int(statistics.mean(hash_rate))
        
        res_difficulty = requests.get(cfg_item("Glassnode", "base_url") + endpoint_difficulty, params=params)
        difficulty_data = res_difficulty.json()
        difficulty_values = [entry['v'] for entry in difficulty_data]
        avg_week_difficulty = int(statistics.mean(difficulty_values))
        
        return avg_week_hash_rate, avg_week_difficulty
        
        
    def market_info(self):
        params = {
            'limit': 1,
            'convert': 'EUR',
            'structure' : 'dictionary'
            }
        endpoint = "https://api.alternative.me/v2/ticker/"
        response = requests.get(endpoint, params=params)
        
        market_data = response.json()
        return market_data
     