import setuptools

setuptools.setup(
    name="ebhook-receiver",
    version="0.0.2",
    license='MIT',
    author="caffeinism",
    author_email="make.dirty.code@gmail.com",
    description="Simple Implementaion of GitHub and GitLab Webhook Receiver",
    #long_description=open('README.md').read(),
    url="https://github.com/MakeDirtyCode/ebhook-receiver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
