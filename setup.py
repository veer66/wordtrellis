from setuptools import setup, find_packages

setup(name="wordtrellis",
      version="0.0.2",
      description="Thai Morpho-syntactic analyzer",
      long_description="""
Thai Morpho-syntactic analyzer
""",
      author="Vee Satayamas",
      author_email="vsatayamas@gmail.com",
      packages=['wordtrellis'],
      package_dir={'wordtrellis': 'wordtrellis'},
      package_data={'wordtrellis': ['rules/*']},
      test_suite="nose.collector")
