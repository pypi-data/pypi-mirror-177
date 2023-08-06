import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vpscli",
    version="0.2.8dev2",
    author="slipper",
    author_email="r2fscg@gmail.com",
    description="VPS manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/vpsinit",
    packages=setuptools.find_packages(),
    package_data={
        setuptools.find_packages()[0]:
        ['data/*.txt', 'data/cauth', 'data/gost.sh']
    },
    install_requires=[
        'endlessh', 'redis', 'pymysql', 'codefast', 'joblib', 'psutil', 'argparse',
        'uuidentifier', 'aiohttp', 'aiomysql', 'aioredis', 'aiofile',
    ],
    entry_points={
        'console_scripts': [
            'vpsinit=vps.__init__:main',
            'vpsstatus=vps.status:status',
            'vpspanel=vps.client:client',
            'nfipsearch=vps.netflix.find_good_ip:entry',
            'primeproduce=vps.primeproducer:entry',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
