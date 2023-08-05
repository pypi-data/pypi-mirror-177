from distutils.core import setup
setup(
  name = 'kumbio_communications',         # How you named your package folder (MyLib)
  packages = ['kumbio_communications'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python module to be able to communicate between Kumbio apps',   # Give a short description about your library
  author = 'Andres Melendes',                   # Type in your name
  author_email = 'andresruse18@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Utalkto/kumbio_communications',   # Provide either the link to your github or to your website
  keywords = ['kumbio'],   # Keywords that define your package best
  install_requires=['phonenumbers'],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.10',
  ],
)


# python setup.py sdist
# twine upload --skip-existing dist/*