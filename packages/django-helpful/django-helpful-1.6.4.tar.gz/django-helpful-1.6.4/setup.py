from setuptools import setup, find_packages

# python3 -m pip install --upgrade twine
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository pypi dist/*
# rm -r build/
# rm -r dist/
# rm -r django_helpful.egg-info


setup(
    name="django-helpful",
    version="1.6.4",
    description="Django helpful things",
    long_description=open("README.rst").read(),
    author="Stanislav Baltrunas",
    author_email="stanislav@baltrunas.ru",
    license="BSD",
    url="https://github.com/Baltrunas/django-helpful",
    # package_dir={"": "helpful"},
    packages=["helpful", "helpful.templatetags"],
    package_data={"templates": ["*"], "static": ["*"], "locale": ["*"], "docs": ["*"],},
    include_package_data=True,
    install_requires=[],
    python_requires=">=2.6, <4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
