from setuptools import setup

setup(
    name='EasyCodrone-EduCommands',
    version='0.0.5',
    packages=['easycodronecommands'],
    url='https://github.com/burgerface627/EasyCodroneEduCommands',
    license='MIT',
    author='Alex Birdsall',
    author_email='burgerface627@outlook.com',
    description='Creates simple commands to be used with Codrone-edu',
    long_description="Creates simple commands to be used with Codrone-edu in order to make movements and certain "
                     "processes simpler and less tedious",
    install_requires=["codrone-edu"]
)
