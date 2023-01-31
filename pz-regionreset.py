#!/usr/bin/env python3

# Summary: Deletes the map files associated with major towns on the default PZ
# map so that they can be regenerated

from math import floor
import os.path

# pairs of coordinates that enclose each major town
REGIONS = {
    'muldraugh': ((10580, 10680), (11090, 8800)),
    'rosewood': ((7900, 11800), (8500, 11200)),
    'westpoint': ((11090, 7000), (12200, 6600)),
    'riverside': ((5800, 5600), (6860, 5180)),
}

def get_region_selection():
    regions_to_clear = []
    selection_done = False

    while not selection_done:
        print('Enter a comma-separated list of towns to reset, \'all\' to reset all major towns, or \'quit\' to cancel')
        print('Valid regions are:')

        for t in REGIONS:
            print(f' - {t}')

        print(' > ', end='')
        line = input().strip()

        if line.lower() == 'quit':
            exit(0)

        towns = [ t.strip() for t in line.lower().split(',') ]

        if len(towns) > 0 and towns[0] == 'all':
            # Add all regions
            regions_to_clear = list(REGIONS.values())
            selection_done = True
        else:
            for t in towns:
                if t in REGIONS:
                    regions_to_clear.append(REGIONS[t])
                else:
                    regions_to_clear = []
                    print(f'Invalid region name \'{t}\'')
                    continue

            selection_done = True

    return regions_to_clear

def get_bin_files_for_region(c1, c2):
    files = []
    xmin, xmax = floor(min(c1[0], c2[0]) / 10), floor(max(c1[0], c2[0]) / 10)
    ymin, ymax = floor(min(c1[1], c2[1]) / 10), floor(max(c1[1], c2[1]) / 10)

    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            files.append(f'map_{x}_{y}.bin')

    return files

def main():
    print('WARNING: Back up your save before continuing!')
    regions = get_region_selection()

    bin_files = []
    for r in regions:
        bin_files += get_bin_files_for_region(r[0], r[1])

    print(f'{len(bin_files)} files will be erased - type \'Ok\' to confirm')
    if input() != 'Ok':
        exit(0)

    for bf in bin_files:
        if os.path.isfile(bf):
            try:
                os.remove(bf)
            except:
                print('Failed to remove \'{bf}\'')
                exit(1)
        else:
            print(f'Ignoring missing file \'{bf}\'')

if __name__ == '__main__':
    main()
