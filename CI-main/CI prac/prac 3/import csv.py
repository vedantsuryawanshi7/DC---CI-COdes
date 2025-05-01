import csv
from concurrent.futures import ProcessPoolExecutor
from collections import defaultdict

# Read the weather data from CSV
def read_weather_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Map function
def map_function(chunk):
    year_temperature_map = defaultdict(list)
    
    for row in chunk:
        year = int(row['Year'])  # Capitalized
        temperature = float(row['Temperature'])  # Capitalized
        year_temperature_map[year].append(temperature)
    
    return year_temperature_map

# Reduce function
def reduce_function(year_temperature_map):
    year_temperature_extremes = {}
    
    for year, temperatures in year_temperature_map.items():
        max_temp = max(temperatures)
        min_temp = min(temperatures)
        year_temperature_extremes[year] = {'max': max_temp, 'min': min_temp}
    
    return year_temperature_extremes

# Split dataset into chunks
def split_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Main MapReduce execution
def map_reduce(file_path, chunk_size=5):
    data = read_weather_data(file_path)
    
    chunks = list(split_data(data, chunk_size))
    
    with ProcessPoolExecutor() as executor:
        map_results = list(executor.map(map_function, chunks))
    
    combined_map_result = defaultdict(list)
    for result in map_results:
        for year, temperatures in result.items():
            combined_map_result[year].extend(temperatures)
    
    result = reduce_function(combined_map_result)
    
    hottest_year = max(result, key=lambda year: result[year]['max'])
    coolest_year = min(result, key=lambda year: result[year]['min'])
    
    return hottest_year, result[hottest_year], coolest_year, result[coolest_year]

# Run the MapReduce process
if __name__ == "__main__":
    hottest_year, hottest_data, coolest_year, coolest_data = map_reduce('large_weather.csv', chunk_size=5)
    
    print(f"Hottest Year: {hottest_year} with temperature {hottest_data['max']}°C")
    print(f"Coolest Year: {coolest_year} with temperature {coolest_data['min']}°C")
