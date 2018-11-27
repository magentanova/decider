from distutils.core import setup

setup(
    name='Decider',
    version='0.1dev',
    packages=['Decider','Decider.db', 'Decider.db.models'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
)