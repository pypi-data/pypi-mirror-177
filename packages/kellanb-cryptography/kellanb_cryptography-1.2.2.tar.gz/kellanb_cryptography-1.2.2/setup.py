from setuptools import setup, find_packages

VERSION = '1.2.2' 
DESCRIPTION = 'encryption libray'
with open('./README.md','r') as f:
  LD =f.read()
setup(

        name="kellanb_cryptography", 
        version=VERSION,
        author="Kellan Butler",
        author_email="kellanbulter52@gmial.com",
        description=DESCRIPTION,
    long_description=LD,
    long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=["pycryptodome==3.15.0"],
        project_urls={'Source':'https://github.com/kellantech/kellanb-cryptography'},

        
        keywords=['python', 'encryption','aes','chacha20','hmac'],
        classifiers= [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS"
        ]
)
