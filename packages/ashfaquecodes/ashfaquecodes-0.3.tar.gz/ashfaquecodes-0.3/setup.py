from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'ashfaquecodes',         # How you named your package folder (MyLib)
  packages = ['ashfaquecodes'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='GNU GPLv3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository or, https://choosealicense.com/
  description = 'Codes which can be used to increase productivity.',   # Give a short description about your library
  author = 'Ashfaque Alam',                   # Type in your name
  author_email = 'ashfaquealam496@yahoo.com',      # Type in your E-Mail
  url = 'https://github.com/ashfaque/ashfaquecodes',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ashfaque/ashfaquecodes/archive/refs/tags/v_03.tar.gz',    # Link of your source code
  keywords = ['ASHFAQUE', 'ASHFAQUECODES', 'PRODUCTIVITY'],   # Keywords that define your package best
  install_requires=[            # Your packages dependencies
          'colorama'
          ,
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)