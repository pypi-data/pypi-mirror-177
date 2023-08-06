from setuptools import setup

setup(
    name='StringToNumber',
    packages=['StringToNumber'],
    version='1.0.0',
    license='MIT',
    description='easy math library',
    author='Luka',
    author_email='app6onpython@gmail.com',
    keywords=['string', 'math', 'String', 'Math', 'number',
              'Number', 'to', 'To', 'StringToNumber',
              'stringToNumber', 'string to number', 'String To Number',
              'string to number', 'String to number'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)

# python setup.py sdist
# twine upload --skip-existing dist/*