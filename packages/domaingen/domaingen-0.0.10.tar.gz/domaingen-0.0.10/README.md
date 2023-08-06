# domaingen

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Jeffery Mandrake from GoInfosystems.com (c) 2023

## Examples of How To Use (Alpha Version)

Create a domaingen object and input keywords

```python

from domaingen.domains import DomainGenerator as dg

keywords = ["recipes","cooking","dinner","easy"] # List of keywords
tlds = ['com','net'] # List of top level domain extensions (optional, default is com)

domaingen = DomainGenerator(keywords,tlds)
domains = domaingen.get_domains()
for domain in domains:
    print(domain)


>>>
cookingdinnereasy.net
recipesdinnereasy.com
recipescooking.com
recipesdinner.com
cookingdinner.net
recipesdinner.net
recipescookingeasy.net
cookingeasy.net
cookingeasy.com
recipesdinnereasy.net
recipescookingdinner.com
recipescookingeasy.com
cookingdinner.com
recipescooking.net
recipescookingdinner.net
recipeseasy.net
dinnereasy.com
cookingdinnereasy.com
dinnereasy.net
recipeseasy.com

```

## Thesaurus (English)
This is a json dataset of synonyms for english words.
Source:
https://www.kaggle.com/datasets/behcetsenturk/englishengen-synonyms-json-thesaurus
