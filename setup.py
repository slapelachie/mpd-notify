from setuptools import setup

LONG_DESC = open("README.md").read()

setup(
    name="mpd-notify",
    version="1.0.0a",
    description="Notification wrapper for mpd",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.8",
    ],
    url="https://github.com/slapelachie/mpd-notify",
    author="slapelachie",
    author_email="lslape@slapelachie.xyz",
    license="GPLv2",
    packages=["mpd_notify"],
    entry_points={"console_scripts": ["mpd-notify=mpd_notify.__main__:main"]},
    install_requires=["python-mpd2", "mutagen", "Pillow", "notify2"],
    zip_safe=False,
)
