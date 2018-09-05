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
    packages=['eegprep', 'eegprep.bids'],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="tests"
)