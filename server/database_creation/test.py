from peewee import *
import logging

db = MySQLDatabase('a',
                   user='game_admin',
                   password='@dmiN123',
                   charset='utf8')


class BaseModel(Model):
    class Meta:
        database = db


class Test(BaseModel):
    name = CharField(default="Not specified")


logging.basicConfig(filename='test.log', level=logging.NOTSET)
logging.info('Started')


db.connect()
db.create_tables([Test])

ja = Test(name="Bartek")
ja.save()
ola = Test(name="Ola")
ola.save()

for person in Test.select():
    print(person.name)

print(db.get_primary_keys('test'))

logging.info('Finished')
db.close()