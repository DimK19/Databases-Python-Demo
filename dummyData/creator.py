import faker

fake = faker.Faker()

DUMMY_DATA_NUMBER = 10;
TABLE_NAME = "students";
TABLE_COLUMNS = ["first_name", "last_name", "email"]
content = "";

for _ in range(DUMMY_DATA_NUMBER):
    firstName = fake.first_name()
    lastName = fake.last_name()
    email = fake.ascii_safe_email()
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{firstName}", "{lastName}", "{email}");\n'

with open(f"dummy_data_{TABLE_NAME}.txt", 'w') as f:
    f.write(content)
