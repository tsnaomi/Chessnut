from setuptools import setup

long_description = """
The chess game underlying the Chessnut web app. A highly-extensible
object-oriented chess game.
"""

setup(
    name="chessnut_game",
    version="0.1-dev",
    description="Chessnut Game",
    long_description=long_description,
    # The project URL.
    url='https://github.com/tsnaomi/Chessnut',
    # Author details
    author='William Dougherty',
    author_email='thegeekofalltrades@gmail.com',
    # Choose your license
    #   and remember to include the license text in a 'docs' directory.
    # license='MIT',
    packages=['chessnut_game'],
    install_requires=[
        'setuptools',
        'mock',
    ]
)
