from setuptools import setup, find_packages

setup(
    name='poldark-qt',  # How you named your package folder (MyLib)
    packages=find_packages(),  # Chose the same as "name"
    version='0.11',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Computer Vision Helper Functions',  # Give a short description about your library
    author='poldark',  # Type in your name
    author_email='zhaowwwjian@gmail.com',  # Type in your E-Mail
    keywords=['Computervision', 'facedetection', 'handtracking'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'pandas',
        'tushare'
    ],
)
