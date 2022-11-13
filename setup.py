from setuptools import find_packages, setup

setup(
    name="cify",
    packages=find_packages(),
    version="0.9.5",
    description="Python CI Framework",
    long_description="A framework that provides the ability to easily and reliably implement nature-inspired optimization meta-heuristics.",
    author="David McCleave",
    author_email="davidjmccleave@gmail.com",
    license="MIT",
    url="https://computer-science.pages.cs.sun.ac.za/rw771/2022/22628274-AE3-src",
    keywords="cify, computational intelligence, optimization, nature-inspired",
    install_requires=[
        'numpy>=1.22.4',
        'pandas>=1.4.3',
        'python-dateutil>=2.8.2',
        'pytz>=2022.6',
        'six>=1.16.0',
        'tqdm>=4.64.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
