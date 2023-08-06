# local-functions

Private repositories from diverse functions used for Data Science

poetry export --without-hashes --format=requirements.txt > requirements.txt

## Build the package

poetry build
poetry publish -u USERNAME -p PASSWORD

'''shell
pip install gensim
pip install bunka_superfunctions
'''
