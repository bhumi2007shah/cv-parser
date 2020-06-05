import csv

with open('/skills.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    skills_set = set()
    for row in csv_reader:
        for value in row:
            skills_set.add(value.lower())

    print(skills_set)

with open("new_skills.csv", 'w', newline='\n') as new_skill_file:
    csv_writer = csv.writer(new_skill_file)
    for value in skills_set:
        csv_writer.writerow([value]);
