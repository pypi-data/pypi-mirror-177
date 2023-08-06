
from itertools import combinations
from py_thesaurus import Thesaurus
import whois
import threading
#install_requires=['python-whois', 'py-thesaurus', 'random-proxies'],
#https://pypi.org/project/py-thesaurus/
#https://pypi.org/project/random-proxies/

class DomainGenerator:

    def __init__(self, domain_keywords, tlds=["com"]):
        self.__domain_keywords = domain_keywords # Input: list of domains
        self.__tlds = tlds
        
    def get_domains(self):
        domains = set()
        for tld in self.__tlds:
            for i in range(2,len(self.__domain_keywords)):
                for j in combinations(self.__domain_keywords,i):
                    domains.add(''.join(j) + '.' + tld)
        return domains
        
    def get_synonym_domains(self):
        domains = set()
        self.__synonym_domain_keywords = set()
        for keyword in self.__domain_keywords:
            thesaurus = Thesaurus(keyword)
            synonym = thesaurus.get_synonym()
            print(synonym)
            #self.__synonym_domain_keywords.add(synonym)        
        for tld in self.__tlds:
            for i in range(2,len(self.__synonym_domain_keywords)):
                for j in combinations(self.__synonym_domain_keywords,i):
                    domains.add(''.join(j) + '.' + tld)
        return domains


def main():
    keywords = ["domain","name","generator","best"]
    tlds = ['com']
    #tlds = ['com','net']
    domaingen = DomainGenerator(keywords,tlds)
    
    domains = domaingen.get_domains()
    #domains = domaingen.get_synonym_domains()
    
    for domain in domains:
        print(domain)
    
if __name__=="__main__":
    main()