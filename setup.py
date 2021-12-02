import setuptools

setuptools.setup(
    name='booking_scraper',
    version='',
    url='https://github.com/felixocker/booking_scraper',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    author='felix',
    author_email='felix.ocker@googlemail.com',
    description='bot for scraping hotel data from booking',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        'selenium',
        'prettytable',
    ],
)
