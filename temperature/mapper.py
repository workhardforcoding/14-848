import sys
valid_quality = [0,1,4,5,9]
valid_temperature = [9999]
for line in sys.stdin:
    line = line.strip()
    date = line[15:23]
    temperature = int(line[87:92])
    quality = int(line[92])
    if (temperature not in valid_temperature and quality in valid_quality):
        print('%s\t%d' % (date, temperature))