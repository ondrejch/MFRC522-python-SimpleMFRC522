import setuptools
from pathlib import Path

README_FILE = Path().resolve() / "README.md"


def main():
    long_description = README_FILE.read_text()

    setuptools.setup(
        name="mfrc522",
        version="1.0.0",
        author="Pi My Life Up / Dennis89",
        author_email="straub.dennis1@web.de",
        description="A library to integrate the MFRC522 RFID readers with the Raspberry Pi",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Dennis-89/MFRC522-python-SimpleMFRC522",
        packages=setuptools.find_packages(),
        install_requires=["gpiozero", "spidev"],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
            "Operating System :: POSIX :: Linux",
            "Topic :: System :: Hardware",
        ],
    )


if __name__ == "__main__":
    main()
