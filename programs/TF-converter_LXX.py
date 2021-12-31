import os
import re
import collections
import json
import csv
# from glob import glob
from tf.fabric import Fabric
from tf.convert.walker import CV
# from tf.compose import modify

source_dirs = 'input' # "input" is the name of the input folder that contains the source file
output_dirs = 'output' # "output" is the name of the output folder to which the finished TF files will be dumped into

bo2book = {line.split()[0]:line.split()[1] for line in '''
OTt4 Old_Testament
'''.split('\n') if line} # "OT" is the name of the file in the input folder AND "split()" splits at space

# patts = {'section': re.compile('(\d*):(\d*)\.(\d*)')}

def director(cv):
        
    '''
    Walks through LXX and triggers
    slot and node creation events.
    '''
        
    # process books in order
    for bo, book in bo2book.items():
        
        book_loc = os.path.join(source_dirs, f'{bo}.txt')
        
        print(f'\thandling {book_loc}...')
        
        with open(book_loc, 'r', encoding="utf8") as infile:
            text = [w for w in infile.read().split('\n') if w]
            
        this_book = cv.node('book')
            
        # keep track of when to trigger paragraph, chapter, and verse objects
        # para_track = 1 # keep counts of paragraphs
        prev_book = "Gen" # start at Genesis
        prev_chap = 1 # start at 1
        prev_verse = 1 # start at 1
        prev_subverse = ''
        wrdnum = 0 # start at 0
        this_chap = cv.node('chapter')
        # this_para = cv.node('paragraph')
        this_verse = cv.node('verse')
        this_subverse = cv.node('subverse')
        
        # iterate through words and construct objects
        for word in text:

            wrdnum += 1

            data = word.split('\t')
            # word_data, lemmas = data[:7], data[7:]

            word_data = data[:26] #the number here is the amount of columns
            morphology = ' '.join(data[26:]) #the number here is the amount of columns
            
            # segment out word data
            # bo_code, ref, brake, ketiv, qere, morph, strongs = word_data
            orig_order, book, chapter, verse, subverse, word, lex_utf8, g_cons_utf8, translit_SBL, lemma_gloss, strong, sp, morphology, case, nu, gn, degree, tense, voice, mood, ps, lemma_translit, abc_order, freq_lemma, BOL_lexeme_dict, BOL_gloss = word_data

            # if chapter == "Prolog":
            #     chapter = 0

            subverse == ""


            #try:
            #    verse = int(verse)
            #except ValueError:
            #    subverse = verse[-1:]
            #    verse = verse[:-1]

            if verse == "":
                print(f'{orig_order}: {verse} {subverse}')


            # strongs_lemma, anlex_lemma = ' '.join(lemmas).split('!') # reconstitute lemmas and split on !

            # chapt, verse, wrdnum = [int(v) for v in patts['section'].match(ref).groups()]

            # -- handle TF events --

            # detect book boundary
            if prev_book != book:

                # end subverse
                cv.feature(this_subverse, subverse=prev_subverse)
                cv.terminate(this_subverse)

                # end verse
                cv.feature(this_verse, verse=prev_verse)
                cv.terminate(this_verse)
                
                # end chapter
                cv.feature(this_chap, chapter=prev_chap)
                cv.terminate(this_chap)

                # end book
                cv.feature(this_book, book=prev_book)
                cv.terminate(this_book)
                
                # new book, chapter, verse, and subverse begin
                this_book = cv.node('book')
                prev_book = book
                this_chap = cv.node('chapter')
                prev_chap = chapter
                this_verse = cv.node('verse')
                prev_verse = verse
                this_subverse = cv.node('subverse')
                prev_subverse = subverse
                wrdnum = 1
            
            # detect chapter boundary
            elif prev_chap != chapter:

                # end subverse
                cv.feature(this_subverse, subverse=prev_subverse)
                cv.terminate(this_subverse)
                
                # end verse
                cv.feature(this_verse, verse=prev_verse)
                cv.terminate(this_verse)
                
                # end chapter
                cv.feature(this_chap, chapter=prev_chap)
                cv.terminate(this_chap)
                
                # new chapter, verse, and subverse begin
                this_chap = cv.node('chapter')
                prev_chap = chapter
                this_verse = cv.node('verse')
                prev_verse = verse
                this_subverse = cv.node('subverse')
                prev_subverse = subverse
                wrdnum = 1
            
            # detect verse boundary
            elif prev_verse != verse:

                # end subverse
                cv.feature(this_subverse, subverse=prev_subverse)
                cv.terminate(this_subverse)

                # end verse
                cv.feature(this_verse, verse=prev_verse)
                cv.terminate(this_verse)

                # new verse and subverse begin
                this_verse = cv.node('verse')
                prev_verse = verse
                this_subverse = cv.node('subverse')
                prev_subverse = subverse
                wrdnum = 1

            # detect subverse boundary
            elif prev_subverse != subverse:
                cv.feature(this_subverse, subverse=prev_subverse)
                cv.terminate(this_subverse)
                this_subverse = cv.node('subverse')
                prev_subverse = subverse

                
            # detect paragraph boundary
            # if brake == 'P':
            #     cv.feature(this_para, para=para_track)
            #     cv.terminate(this_para)
            #     this_para = cv.node('paragraph') # start a new paragraph
            #     para_track += 1 # count paragraphs in the book
                
                
            # make word object
            this_word = cv.slot()
            cv.feature(this_word, 

                       orig_order=orig_order,
                       book=book,
                       chapter=chapter,
                       verse=verse,
                       subverse=subverse,
                       word=word,
                       lex_utf8=lex_utf8,
                       g_cons_utf8=g_cons_utf8,
                       translit_SBL=translit_SBL,
                       lemma_gloss=lemma_gloss,
                       strong=strong,
                       sp=sp,
                       morphology=morphology,
                       case=case,
                       nu=nu,
                       gn=gn,
                       degree=degree,
                       tense=tense,
                       voice=voice,
                       mood=mood,
                       ps=ps,
                       lemma_translit=lemma_translit,
                       abc_order=abc_order,
                       freq_lemma=freq_lemma,
                       BOL_lexeme_dict=BOL_lexeme_dict,
                       BOL_gloss=BOL_gloss,

                       
                       # ketiv=ketiv, 
                       # qere=qere, 
                       # strongs=strongs, 
                    #    str_lem=strongs_lemma.strip(),
                    #    anlex_lem=anlex_lemma.strip()
                      )
            cv.terminate(this_word)
        
        # end book and its objects
        # - end subverse
        cv.feature(this_subverse, subverse=prev_subverse)
        cv.terminate(this_subverse)

        # - end verse
        cv.feature(this_verse, verse=prev_verse)
        cv.terminate(this_verse)
        
        # - end paragraph
        # cv.feature(this_para, para=para_track)
        # cv.terminate(this_para)
        
        # - end chapter
        cv.feature(this_chap, chapter=prev_chap)
        cv.terminate(this_chap)
        
        # - end book
        cv.feature(this_book, book=prev_book)
        cv.terminate(this_book)


slotType = 'word'
otext = {'fmt:text-orig-full':'{word} ',
         'sectionTypes':'book,chapter,verse',
         'sectionFeatures':'book,chapter,verse'}

generic = {'Name': 'LXX',
           'Version': '1935',
           'Author': 'Rahlfs',
           'Editors': 'CCAT, Eliran Wong',
           'Converter': 'Adrian Negrea, Oliver Glanz', 
           'Source:':'https://github.com/eliranwong/LXX-Rahlfs-1935',
           'Note':'?'}

intFeatures = {'chapter', 'verse'}

featureMeta = {
                'orig_order': {'description': 'original word order in corpus'},
                'book': {'description': 'book'},
                'chapter': {'description': 'chapter'},
                'verse': {'description': 'verse'},
                'subverse': {'description': 'subverse'},
                'word': {'description': 'text realized word'},
                'lex_utf8': {'description': 'normalized word'},
                'g_cons_utf8': {'description': 'word without accents'},
                'translit_SBL': {'description': 'SBL transliteration'},
                'lemma_gloss': {'description': 'English gloss'},
                'strong': {'description': 'Strong numbers'},
                'sp': {'description': 'part of speech'},
                'morphology': {'description': 'morphology'},
                'case': {'description': 'case'},
                'nu': {'description': 'number'},
                'gn': {'description': 'gender'},
                'degree': {'description': 'degree'},
                'tense': {'description': 'tense'},
                'voice': {'description': 'voice'},
                'mood': {'description': 'mood'},
                'ps': {'description': 'person'},
                'lemma_translit': {'description': 'lemma transliteration'},
                'abc_order': {'description': 'dictionary order'},
                'freq_lemma': {'description': 'frequency of word in corpus'},
                'BOL_lexeme_dict': {'description': 'BOL dictionary form of lemma'},
                'BOL_gloss': {'description': 'BOL English gloss'},
    
               # 'para': {'description': 'A paragraph number'},
               # 'ketiv': {'descrption': 'The text as it is written in the printed Tischendorf'},
               # 'qere': {'description': 'The text as the editor thinks it should have been'},
               # 'strongs': {'description': 'A word\'s number in Strongs'},
               # 'str_lem': {'description': 'Word lemma that corresponds to The NEW Strong\'sComplete Dictionary of Bible Words'},
               # 'anlex_lem': {'description': 'Word lemma that corresponds to Friberg, Friberg and Miller\'s ANLEX'}
              }


# configure metadata/output
version = '1935'
generic['Version'] = version

output = os.path.join(output_dirs, version)

print(f'Processing Version {version}')
output_dir = output_dirs.format(version=version)

TF = Fabric(locations=output_dir, silent=True)
cv = CV(TF)

cv.walk(director,
                slotType,
                otext=otext,
                generic=generic,
                intFeatures=intFeatures,
                featureMeta=featureMeta,
                warn=True,
                force=False,)