import random
import csv

drivers = ['Sammal', 'Kast', 'Murd', 'Kinkar', 'Pregel']
laps = 10
filename = 'Result.csv'
file_header = ['Ring', 'Nimi', 'Aeg', 'Sektor1', 'Sektor2', 'Sektor3', 'Viga']
results = []
minimum_sector_time = 23
maximum_sector_time = 26
fastest_lap = ['Unknown', 999]
fastest_sectors = [['Unknown', 999], ['Unknown', 999], ['Unknown', 999]]
sector_times = []


def generate_random_sector_time(min_time, max_time):
    thousandth = random.randint(0, 999) / 1000
    return random.randint(min_time, max_time) + thousandth


def calculate_lap_time(min_time, max_time, driver_name):
    total_time = 0
    sector_times.clear()
    for i in range(3):
        sector_time = generate_random_sector_time(min_time, max_time)
        if sector_time < fastest_sectors[i][1]:
            fastest_sectors[i][0] = driver_name
            fastest_sectors[i][1] = sector_time
        total_time += sector_time
        sector_times.append(sector_time)
    return total_time


def get_fastest_lap(driver_name, fastest_data):
    if driver_name == fastest_data[0]:
        return format_time(fastest_data[1])
    else:
        return ""


def format_time(seconds, num_milliseconds=3):
    if hasattr(seconds, '__len__'):
        return [format_time(s) for s in seconds]
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if num_milliseconds > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (num_milliseconds + 3, num_milliseconds)
    else:
        pattern = r'%02d:%02d:%02d'
    if days == 0:
        return pattern % (hours, minutes, seconds)
    return ('%d days, ' + pattern) % (days, hours, minutes, seconds)


if __name__ == '__main__':
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(file_header)
        for driver in drivers:
            lap_time_total = 0
            error_laps = []
            for lap in range(laps):
                has_error = False
                if random.randint(0, 9) == 2:
                    lap_time_total += calculate_lap_time(30, 90, 'Unknown')
                    error_laps.append(lap + 1)
                    has_error = True
                else:
                    this_lap_time = calculate_lap_time(minimum_sector_time, maximum_sector_time, driver)
                    if this_lap_time < fastest_lap[1]:
                        fastest_lap[0] = driver
                        fastest_lap[1] = this_lap_time
                    lap_time_total += this_lap_time
                row = [lap + 1, driver, sum(sector_times), sector_times[0], sector_times[1], sector_times[2], has_error]
                writer.writerow(row)
            results.append([driver, lap_time_total, error_laps])

    results = sorted(results, key=lambda x: x[1])

    for index, driver_info in enumerate(results):
        if index > 0:
            time_difference = format_time(driver_info[1] - results[0][1])
            print(driver_info[0].ljust(10), format_time(driver_info[1], 3), time_difference, driver_info[2],
                  get_fastest_lap(driver_info[0], fastest_lap))
        else:
            print(driver_info[0].ljust(10), format_time(driver_info[1], 3), driver_info[2],
                  get_fastest_lap(driver_info[0], fastest_lap))

    print('Sektorite parimad')
    total_time = 0
    for index, driver in enumerate(fastest_sectors):
        total_time += driver[1]
        print('Sektor', (index + 1), driver[0].ljust(10), format_time(driver[1]))
    print('Unelmate ring', format_time(total_time))
