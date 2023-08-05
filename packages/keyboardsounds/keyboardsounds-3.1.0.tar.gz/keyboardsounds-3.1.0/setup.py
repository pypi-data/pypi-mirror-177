from setuptools import setup

setup(
   name='keyboardsounds',
   version='3.1.0',
   description='Adds the ability to play sounds while typing on any system.',
   author='Nathan Fiscaletti',
   author_email='nate.fiscaletti@gmail.com',
   packages=['keyboardsounds'],
   install_requires=['pygame', 'pynput', 'psutil', 'imageio-ffmpeg'],
   package_data={
    'keyboardsounds': [
      'profiles/ios/*',
      'profiles/typewriter/*'
    ],
   },
   entry_points={
         'console_scripts': [
                'keyboardsounds = keyboardsounds.main:main',
         ],
   },
)
