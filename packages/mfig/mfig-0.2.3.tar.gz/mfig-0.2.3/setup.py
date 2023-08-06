from setuptools import setup, find_packages

with open('./Readme.md') as f:
    txt = f.read()

setup(name='mfig',
      version='0.2.3',
      description='A tool for merging multiple figures into one',
      long_description=txt,
      long_description_content_type='text/markdown',
      author='Koushik Naskar',
      author_email='koushik.naskar9@gmail.com',
      license="MIT",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console', 
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: System :: Shells',
          'Programming Language :: Python :: 3.6'
      ],
      keywords='Image merging',
      project_urls={'Source Code': 'https://github.com/Koushikphy/mfig'},
      zip_safe=True,
      python_requires='>=3.6',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'mfig = mfig.mfig:main',
          ],
      })
