try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    

requires = []
with open('requirements.txt') as reqfile:
    requires = reqfile.read().splitlines()

setup(
    name='eegprep',
    version='0.1',
    description='Standarized EEG preprocessing',
    url='https://github.com/Charestlab/eegprep',
    long_description='',
    classifiers=[
      "Programming Language :: Python",
      ],
    author='',
    author_email='',
    keywords='analysis eeg BIDS',
    packages=['eegprep'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'eegprep = eegprep.main:run',
        ],
    },
    tests_require=requires,
    test_suite="tests"
)
