from setuptools import setup

setup(
    name='estim8Beta',
    version='0.0.1',
    py_modules=["estim8", "models", "utils", "visualization", "optimizers"],
    description='Conduct parameter estimations for Dymola and FMU models',
    author='Daniel Strohmeier',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'openpyxl',
        'joblib',
        'pathlib',
        'matplotlib',
        'seaborn',
        'fmpy',
        'sdf',
        'notebook',
    ],
)