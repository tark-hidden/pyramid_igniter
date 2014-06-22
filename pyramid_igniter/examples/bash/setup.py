import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid-igniter',
    'pyramid_jinja2',
    'markupsafe',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='bash',
      version='0.1',
      description='igniter_example',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Tark',
      author_email='tark.hidden@gmail.com',
      url='',
      keywords='web wsgi pyramid bootstrap',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='igniter_example',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = bash:main
      [console_scripts]
      initialize_bash_db = bash.scripts.initializedb:main
      """,
      )
