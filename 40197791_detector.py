import os
import sys
import re
import math
import time

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

#detect if text is code given text file path
def detectIsSourceCode(path):
    count = 0
    countline = 0
    specialops = [ "&&", "||", "==", "!=", ">=", "<=", ">>", "<<", "::", "__"]
    comments = ["/*" , " //", " #", " <!--"]
    with open(path) as file:
        for line in file: 
            countline+=1
            if line.endswith(';') or line.endswith('{') or line.startswith('{') or line.startswith('}') or line.endswith(':'):
                count +=1
            elif re.search('[a-zA-Z]*\([a-zA-z]*\)', line):   #myFunc() syntax check
                count +=1
            elif re.search('[a-zA-Z]*\.[a-zA-z]*\=[a-zA-Z]*\->[a-zA-z]*', line):   #foo.bar = ptr->val syntax check
                count +=1
            elif any(op in line for op in specialops):    #checks for special operations
                count +=1
            elif any(op in line for op in comments):    #checks for comment 
                count +=1
        
        percentCode = ( count / countline ) * 100
        if percentCode >= 20:
            return True
        else: 
            return False

#filter references from source text
def filterReferences(path):
    filteredContent = ""
    with open(path) as file:
        for line in file:
            if " ed." not in line and " eds." not in line:
                filteredContent +=line
    pattern_list = [r'((.*)\. (\d{4})\.)', r'((\"[a-zA-Z0-9]+\"))', r'\([^()\d]*\d[^()]*\)']
    matches = []
    for r in pattern_list:
        found = re.findall( r, filteredContent)
        if len(found) > 0:
            for string in found:
                filteredContent = filteredContent.replace(str(string), "")
        matches+=found
    return filteredContent, matches

#filter stop words, special characters and direct quotation sentences
def filterstopwords(path):
    #filter references from text
    filteredContent, references = filterReferences(path)
    filewords = filteredContent.split()
    filteredwordlist = []

    #filter special characters
    patternspecialchar = '\"\'!@#$%^&*()[]{};:,./<>?\|`~-=_+'
    quotationRemoved = False
    pattern3 = r'(\"[a-zA-Z0-9]+\")'
    referencesFound = True if len(references) > 0 else False
    for word in filewords:
        if referencesFound == False and word.lower() not in stopwords:
            filteredwordlist.append(word.lower().translate ({ord(c): "" for c in patternspecialchar}))
        else:
            if word.startswith('"') or word.startswith("'"):
                quotationRemoved = True
                if re.findall(pattern3, word):
                    quotationRemoved = False
            elif word.endswith('"') or word.endswith("'"):
                quotationRemoved = False
            elif word.lower() not in stopwords and quotationRemoved==False:
                filteredwordlist.append(word.lower().translate ({ord(c): "" for c in patternspecialchar}))

    #file is completely referenced, just filter stop words and special characters    
    if referencesFound and len(filteredwordlist) == 0:
        for word in filewords:
            if word.lower() not in stopwords:
                filteredwordlist.append(word.lower().translate ({ord(c): "" for c in patternspecialchar}))
    return filteredwordlist

def preprocessSourceCode(path):
    return open(path).read().split()

#LCS calculate longest common subsequence between two array of words
def lcs(s1, s2):
    l1 = len(s1)
    l2 = len(s2)
    dlcs = [[None] * (l2 + 1) for i in range(l1 + 1)]

    for i in range(l1 + 1):
        for j in range(l2 + 1):
            if i == 0 or j == 0:
                dlcs[i][j] = 0
            elif s1[i - 1] == s2[j - 1]:
                dlcs[i][j] = dlcs[i - 1][j - 1] + 1
            else:
                dlcs[i][j] = max(dlcs[i - 1][j], dlcs[i][j - 1])

    return dlcs[l1][l2]

def main(inputFileList):
    srcPath = os.path.abspath(inputFileList[1])
    comparePath = os.path.abspath(inputFileList[2])

    #length of files
    srclen = len(open(srcPath).read().split())
    destlen = len(open(comparePath).read().split())

    #check source file being code and generate tokens
    srctokens = []
    comparetokens = []
    if detectIsSourceCode(srcPath):
        srctokens = preprocessSourceCode(srcPath)
        comparetokens = preprocessSourceCode(comparePath)
    else:
        srctokens = filterstopwords(srcPath)
        comparetokens = filterstopwords(comparePath)

    #run LCS on tokens
    lcs_val = lcs(srctokens, comparetokens)
    plagPercent = (lcs_val/math.sqrt(srclen * destlen))*100
    if plagPercent > 20:
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("-1")
        exit()
    main(sys.argv)