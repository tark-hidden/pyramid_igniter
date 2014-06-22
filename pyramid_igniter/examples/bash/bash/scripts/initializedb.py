import os
import sys

from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars
from bash.models import dbs, Base, StaffModel
import transaction


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    dbs.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = StaffModel(
            id=1, role='admin', name='admin',
            password='993b33d7c0fc53d51125255feae9b9'
                     '4ce5213c2269d254b895c423c87035610e',
            salt='666')
        dbs.add(model)

    # session.commit()
