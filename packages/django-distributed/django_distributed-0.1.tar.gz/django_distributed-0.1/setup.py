from setuptools import setup

setup(name='django_distributed',
      version='0.1',
      description='A python for distributed databases setup in Django',
      url='https://github.com/lodlaw/django-distributed',
      author='Anh Pham',
      author_email='anh.pham@lodlaw.com',
      license='MIT',
      packages=['django_distributed', 'django_distributed.router'],
      install_requires=[
          'django-crum',
          'django',
      ],
      zip_safe=False)
