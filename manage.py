from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from ptpython.ipython import embed

from app import db, create_app
from app.models import User, Item, Bucketlist

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


# Thanks to :
# http://stackoverflow.com/questions/33708004/how-can-i-use-ptipython-with-flask-script-together
class PtShell(Shell):
    """
    This is a custom shell based on ptpython shell.

    Integration with ptpython offers an enhanced user experience when
    interacting with the application on a command line shell environment.

    The models classes have been added to the shell environment. These do not
    need to be imported when the application is run via `python manage.py shell`
    """
    def run(self, **kwargs):
        context = self.get_context()
        context.update(db=db, User=User, Item=Item, Bucketlist=Bucketlist)
        embed(user_ns=context)


manager.add_command('shell', PtShell())

if __name__ == '__main__':
    manager.run()

