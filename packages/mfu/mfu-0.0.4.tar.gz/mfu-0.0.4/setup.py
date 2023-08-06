from setuptools import setup, find_packages

setup(
    name='mfu',
    description='Michael\'s fun utilities',
    version='0.0.4',
    author="Michal Botha",
    author_email='michael@408.co.za',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click >= 8.1.3',
        'kubernetes >= 25.3.0',
        'watchdog >= 2.1.9',
        'GitPython >= 3.1.29'
    ],
    entry_points={
        'console_scripts': [
            'mfu = mfu.main:cli',
        ],
    },
)
