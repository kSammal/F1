def sec2time(sec, n_msec=3):
    # https://stackoverflow.com/a/33504562
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


results = []

# Read results from file
with open("Result.txt", "r") as file:
    next(file)  # Skip header line
    for line in file:
        line = line.strip().split(";")
        result = [int(line[0]), line[1], float(line[2]), float(line[3]), float(line[4]), float(line[5]),
                  line[6] == "True"]
        results.append(result)

# Fastest lap racer
fastest_lap = min(results, key=lambda x: x[2])
print("Fastest Lap Racer:")
print(f"Name: {fastest_lap[1]}")
print(f"Lap Time: {fastest_lap[2]} seconds")
print()

# Top 5 racers
sorted_results = sorted(results, key=lambda x: x[2])[:5]
print("Top 5 Racers:")
for i, racer in enumerate(sorted_results):
    print(f"{i + 1}. {racer[1]} - Lap Time: {racer[2]} seconds")
print()

# Sectors best
best_sectors = []
for i in range(3, 6):
    sector_best = min(results, key=lambda x: x[i])
    best_sectors.append((sector_best[1], sector_best[i]))

print('Fastest sector')
total = 0
for idx, driver in enumerate(best_sectors):
    total += driver[1]  # Add up sector times for one lap
    # Show sector information
    print('Sector', (idx + 1), driver[0].ljust(10), sec2time(driver[1]))

print('Dream lap time', sec2time(total))  # Total dream lap time
