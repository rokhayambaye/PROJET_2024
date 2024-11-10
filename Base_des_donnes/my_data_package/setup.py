#%%
# setup.py
from setuptools import setup, find_packages

setup(
    name='my_data_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',  # Ajoutez d'autres dépendances si nécessaire
    ],
    entry_points={
        'console_scripts': [
            'download-data=my_data_package.downloader:download_data',
        ],
    },
    description='Package pour télécharger les données des compteurs de Montpellier',
    author='Mbaye',
    author_email='mbayerokhaya416@example.com',
    url='https://github.com/coralieromani/PROJET_2024',
)

# %%
