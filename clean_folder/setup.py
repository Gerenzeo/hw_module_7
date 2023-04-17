from setuptools import setup, find_namespace_packages

setup(
    name='Cleaner',
    description='Clean folder - performs the function of sorting files into the specified path.',
    version='0.0.3',
    author='Artem Ivanina',
    author_email='artem.ivanina1994@gmail.com',
    url='https://github.com/Gerenzeo',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'cleanfolder=clean_folder.clean:main'
    ]}
)