from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pyrampl',
    version='1.31',
    description='Python Random Access Machine programming language',
    keywords='random access machine simulation',
    author='Samy Zafrany',
    #url='https://www.samyzaf.com/afl/pyrampl.html',
    author_email='sz@samyzaf.com',
    license='MIT',
    packages=['pyrampl'],
    zip_safe=False,
)

