import random


def is_fastest_lap(driver_name, fastest_data):
    if driver_name == fastest_data[0]:
        return sec2time(fastest_data[1])
    else:
        return ""


def sec2time(sec, n_msec=3):
    if hasattr(sec, '__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec + 3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)


if __name__ == '__main__':
    Filename = 'Result.txt'
    results = []
    fastest_lap = ['Unknown', 9999]
    three_sektors = [['Unknown', 9999], ['Unknown', 9999], ['Unknown', 9999]]
    lap_times = {}
    lap_errors = {}

    with open(Filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        File_header = lines[0]
        for line in lines[1:]:
            data = line.strip().split(';')
            lap = int(data[0])
            name = data[1]
            lap_time = float(data[2])
            sector1 = float(data[3])
            sector2 = float(data[4])
            sector3 = float(data[5])
            error = True if data[6].lower() == 'true' else False
            if lap_time < fastest_lap[1]:
                fastest_lap[0] = name
                fastest_lap[1] = lap_time
            if sector1 < three_sektors[0][1]:
                three_sektors[0][0] = name
                three_sektors[0][1] = sector1
            if sector2 < three_sektors[1][1]:
                three_sektors[1][0] = name
                three_sektors[1][1] = sector2
            if sector3 < three_sektors[2][1]:
                three_sektors[2][0] = name
                three_sektors[2][1] = sector3

            if name not in lap_times:
                lap_times[name] = 0
            lap_times[name] += lap_time

            if error:
                if name not in lap_errors:
                    lap_errors[name] = []
                lap_errors[name].append(lap)

            results.append([name, lap_time, error])

    lap_times = sorted(lap_times.items(), key=lambda x: x[1])

    rank = 1
    for idx, (name, total_time) in enumerate(lap_times):
        time_difference = sec2time(total_time - fastest_lap[1])
        error_laps = lap_errors.get(name, '[]')
        time_difference_from_first = sec2time(total_time - lap_times[0][1])
        fastest_lap_str = is_fastest_lap(name, fastest_lap)

        if idx == 0:
            print(rank, name.ljust(10), sec2time(total_time), error_laps, fastest_lap_str)
        else:
            difference = sec2time(total_time - lap_times[0][1])
            print(rank, name.ljust(10), sec2time(total_time), difference, error_laps, fastest_lap_str)

        rank += 1

    print('\nSektori parimad')
    total = sum(driver[1] for driver in three_sektors)
    for idx, driver in enumerate(three_sektors):
        print('Sektor', (idx + 1), driver[0].ljust(10), sec2time(driver[1]))
    print('Unelmate Ring', sec2time(total))
