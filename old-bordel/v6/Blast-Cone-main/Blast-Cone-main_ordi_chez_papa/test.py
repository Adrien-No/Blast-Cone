import csv

with open('test.csv','w') as file:
    fieldnames = ['guild_id','channel_id']
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'guild_id': 505477568195985411, 'channel_id': 525382426252279809})
    
with open('test.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['guild_id'],row['channel_id'])

with open('test.csv','w') as file:
    fieldnames = ['guild_id','channel_id']
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'guild_id': 505477568195985411, 'channel_id': 525382426252279809})

with open('test.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['guild_id'],row['channel_id'])
