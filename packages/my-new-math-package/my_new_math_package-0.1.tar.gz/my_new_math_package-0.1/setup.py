from setuptools import setup, find_packages

setup(name='my_new_math_package',
      version='0.1',
      description='simple math',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)


# https://towardsdatascience.com/how-to-upload-your-python-package-to-pypi-de1b363a1b3 - это залив проекта на pypi
# когда написан весь код, в терминале необходимо  python -m pip install --user --upgrade setuptools wheel twine
# затем  python setup.py sdist bdist_wheel
# потом twine upload dist/*   и теперь у тебя на pypi лежит реп с этим пакетом. Другие пользователи смогут его импортить


