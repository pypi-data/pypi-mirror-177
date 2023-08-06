from setuptools import setup

setup(
    name='nonestrap',
    version=open('VERSION').read(),
    description='Another NoneBot2 project bootstrap tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HivertMoZara',
    author_email='worldmozara@gmail.com',
    url='https://github.com/NCBM/nonestrap',
    scripts=['nonestrap.py'],
    entry_points={
        'console_scripts': [
            'nonestrap = nonestrap:_entry'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    license='MIT',
)
