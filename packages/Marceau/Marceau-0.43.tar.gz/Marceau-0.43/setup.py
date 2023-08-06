from distutils.core import setup
setup(
  name = 'Marceau',         # How you named your package folder (MyLib)
  packages = ['Marceau'],   # Chose the same as "name"
  version = '0.43',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Panjer's Algorithm in Python",   # Give a short description about your library
  author = 'Rayane Vigneron',                   # Type in your name
  author_email = 'rayanevigneron@yahoo.fr',      # Type in your E-Mail
  url = 'https://github.com/despervita/Marceau',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/despervita/Marceau/archive/v_043.tar.gz',    # I explain this later on
  keywords = ['Panjer', 'Python'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.9' ,     #Specify which pyhton versions that you want to support

  ],
)