import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='qr-fileautomator',
    version='3.6.2',
    author='S.chaudhary',
    author_email='chaudharyshivshankarex09@gmail.com',
    description='Transfer files over WiFi between your computer and your smartphone from the terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['qr-filetransfer = qr_filetransfer:main']},
    install_requires=['qrcode', 'colorama; platform_system == "Windows"'],
    extras_require={'extras': ['netifaces']}
)
