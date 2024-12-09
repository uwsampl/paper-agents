from setuptools import setup, find_packages

setup(
    name='paper_agents',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'paper_agents=paper_agents.__main__:main',
        ],
    },
    install_requires=[
        # Add your project dependencies here
        "openai",
    ],
)
