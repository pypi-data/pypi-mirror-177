import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='CRISPRbean',  
     version='0.1.0',
     author="Jayoung Ryu",
     author_email="jayoung_ryu@g.harvard.edu",
     description="CRISPR Base Editing with Acticity Normalization",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/jykr/beige",
     packages=setuptools.find_packages(),
     scripts=["bin/CRISPRbean"],
     install_requires=[
        'pyro-ppl',
        'numpy',
        'berets'
      ],
      include_package_data=True,
    #package_data={'': ['beret/annotate/ldlr_exons.fa']},
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )

