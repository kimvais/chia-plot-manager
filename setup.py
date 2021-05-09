from distutils.core import setup

setup(
    name='chia-plot-manager',
    version='1.0',
    packages=['plotmanager', 'plotmanager.library', 'plotmanager.library.parse', 'plotmanager.library.commands',
              'plotmanager.library.utilities'],
    url='https://gitlab.com/kimvais/chia-plot-manager',
    license='GPLv3',
    install_requires=[
        "dateparser==1.0.0",
        "discord_notify==1.0.0",
        "playsound==1.2.2",
        "psutil==5.8.0",
        "python_pushover==0.4",
        "PyYAML==5.4.1",
        ],
    author='Kimmo Parviainen-Jalanko',
    author_email='kimvais@kimva.is',
    description='Chia plot manager'
    )
