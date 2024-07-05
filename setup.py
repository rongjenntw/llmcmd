from setuptools import setup, find_packages

setup(
    name='llmcmd',
    version='0.1',
    packages=find_packages(),
    description='This program provides means to interact with llm on terminal.',
    author='Rong-Jenn Chang',
    author_email='rongjenn@gmail.com',
    entry_points={
        'console_scripts': [
            'my_package_command = llmflows:main'
        ]
    }
)