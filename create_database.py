import sys
from sqlalchemy_utils import database_exists, create_database
from database import engine, Base
from models.user import User
from models.room import Room, room_transit

__author__ = 'ohaz, popup'

opt_replace = False

# Parsing command line options
for argit in sys.argv:
    if argit == '-r' or argit == '--replace':
        opt_replace = True
    elif argit == '-h' or argit == '--help':
        print('IRD Database creation tool')
        print()
        print('  -r\t--replace\tReplaces existing database')
        print()
        exit()


if __name__ == '__main__':

    if not (database_exists(engine.url) and not opt_replace):
        print('Creating DB')
        create_database(engine.url)
        Base.metadata.create_all(engine)
    else:
        print('DB exists. Run \'' + sys.argv[0] + '\' -r to replace.')
