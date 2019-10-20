from server.database_creation.models.Models import *

logging.basicConfig(filename='functionality.log', level=logging.NOTSET)
logging.info(' [{}] Started'.format(str(datetime.datetime.now())))
models = [User, Character, Blueprints, ItemsInGame, Enemy, NonPersonCharacter]
print(uuid.uuid4())
db.connect()

db.drop_tables(models=models)

db.create_tables(models=models)

superuser = User(username="Not2hy", password="test123")
other = User(username="Nn2n", password="123456789")
superuser.save(force_insert=True)
other.save(force_insert=True)

db.close()
logging.info(' [{}] Finished'.format(str(datetime.datetime.now())))
