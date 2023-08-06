from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='servo-config-reader',
    version='0.0.1',
    packages=['servo_config_reader'],
    url='https://github.com/Adam-Software/Servo-config-reader',
    license='MIT',
    author='vertigra',
    author_email='a@nesterof.com',
    description='Read position range config',
    long_description_content_type="text/markdown",
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
