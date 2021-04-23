#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 18:44:56 2021

@author: lucie
"""



from lxml import etree
#import operator




#tree = etree.parse("../LEXIQUES/Wiktionnaire/GLAWI-test.xml")
tree = etree.parse("../LEXIQUES/Wiktionnaire/GLAWI_FR_work_D2015-12-26_R2016-05-18.xml")

root = tree.getroot()
pos = {}
wikt = {}


def find_sens_labelise(dic):
    for vs in dic.values():
        if (vs.find('diachronic') != -1) and (vs.find('sem') != -1):
            return 1
    return 0


def print_ul (dic) :
        for cl, vl in dic.items():
            print(vl, end=' ')
        print()
        


def is_polycat(brothers) :
    other_cat="no"
    count_nouns=0
    #pas d'homonyme 
    if len(brothers) == 1 :
        return 0
    else :
        for pos1 in brothers :
            if (pos1.get("type") != 'verbe'):
                other_cat = "yes" 
            else :
                count_nouns = count_nouns+1
    # homonyme nominal + homonyme d'une autre catégorie            
    if other_cat == "yes" and count_nouns > 1 :
        return 1
    # homonyme d'une autre catégorie            
    elif other_cat == "yes" :
        return 1
    # homonyme nominal
    else :
        return 0


def is_evol_candidate(definitions):
#    print(definitions)
    label_diachronic=0
    label_sem=0
    
    for defi in definitions :
        for label in defi.iter('label'):
            if label.get('type') == "diachronic" :
                label_diachronic = 1
            if label.get('type') == "sem" :
                label_sem = 1
    
    if label_diachronic == 1 and label_sem == 1 :
        return 1
    else:
        return 0



for article in root.xpath("//article"):
    for pos in article.iter('pos'):
        if pos.get("type") == 'verbe' and pos.get("lemma").find("1") != -1 :


            # on ne retient pas les formes nominales ambigues (avec une autre POS)
            if (is_polycat(pos.findall("../pos")) == 1) :
                break
            else:           
                # on retient comme canditats les lemmes ayant au moins un sens marqué d'un label "diacronic" et un sens marqué d'un label "sem"
                if(is_evol_candidate(pos.iter('definition')) == 1) :
                    print(article.find("title").text)



 





