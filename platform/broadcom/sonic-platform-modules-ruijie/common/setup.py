from setuptools import setup

setup(
    name='sonic-platform',
    version='1.0',
    description='SONiC platform API implementation on Ruijie B6510-48VS8CQ Platforms',
    license='Apache 2.0',
    author='SONiC Team',
    author_email='sonic_rd@ruijie.com.cn',
    url='',
    maintainer='Ruijie B6510-48VS8CQ',
    maintainer_email='',
    packages=[
        'sonic_platform',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    keywords='sonic SONiC platform PLATFORM',
)
