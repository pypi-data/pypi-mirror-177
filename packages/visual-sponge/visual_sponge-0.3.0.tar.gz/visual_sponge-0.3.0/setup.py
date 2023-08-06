from setuptools import setup, find_packages

setup(name="visual_sponge",
      version="0.3.0",
      description="A python package to do the visualization for molecular simulations",
      author="Yijie Xia",
      author_email="yijiexia@pku.edu.cn",
      packages=find_packages(),
      package_data = {"":['*.css', '*.js', '*.html', '*.ico', '*.ini']},
      install_requires = ["flask", "Xponge", "pyffmpeg"],
      long_description=open('README.md').read(),
      entry_points = {
        "console_scripts": ["visual-sponge = visual_sponge.__main__:main"]},
      classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        'Development Status :: 5 - Production/Stable',
        "Operating System :: OS Independent",
        ],
      python_requires='>=3.6',
      )