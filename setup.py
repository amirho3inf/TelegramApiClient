import setuptools

long_description = open("README.md", "r").read()
install_requires = ['telepot==12.6']
setuptools.setup(
    name="TelegramApiBot",
    version="1",
    author="AmirHo3inF",
    author_email="MrAmirho3inf@gmail.com",
    description="Telepot upgraded version",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amirho3inf/TelegramApiClient",
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License"
    ),
)
