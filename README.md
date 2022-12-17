# COMP6651
Plagiarism-detector: The algorithm takes two files as input, uses dynamic programming to compare them and checks if they are plagiarized. It returns 1 if they are found plagiarized otherwise 0

# 1. What the algorithm does?
## 1.1 Algorithm used:
    It uses Longest common subsequence at its core and compare two files with word based tokenization. 
## 1.2 Preprocessing
    It first detects if text is code?
    If it is code, it simply applies space based tokenization to the text. 
    If it is not detected as code, it applies a series of preprocessing:
        First it detects references in files, example: book references, author references using regular expressions and filters out those content. As the reference content should not be considered in plagarism detection.
        The algorithm also filters out punctuations and stopwords from tokens which is tokenized using space. 
        It also removes quotation references as they are majorly a part of direct references to author's work which increases plagiarism score.
## 1.3 Longest common subsequence
    LCS is used for word to word comparison of text after preprocessing, which gives us the Longest common subsequence length based on matching words.
## 1.4 Decision Plagarized/Non - Plagiarized?
    It then applies math.sqrt(source token length * compare token length) and finds percentage of plagiarism based on size of both files.
    If the threshold > 20% then it declares file as plagiarized, not plagiarized otherwise

## 2. What challenges faced during development?
    The text file being source code or text based on regular expression is not a robust method to detect, detecting code using file extensions can be a better way. 
    Also references filter is not robust as it just captures a limited reference patterns and does not captures semantics of sentence to detect is it is an actual reference or not.
    The quotation references filter helped a lot in not affecting the plagiarism percentage, as it is not generic we may lead to true negative examples of plagiarism.

## 3. Project file structure:
    |--COMP6561
        |----40197791_detector.py   // detector file
        |----Makefile               // file that executes terminal commands
        |----README.txt             // contains information about how algorithm works, how to run the project
    |--data                         // data folder containing test files
        |----okay01                 //folder containing non plagiarized files
            |----1.txt
            |----2.txt
        .
        .
        .
        |----okay06                 
            |----1.txt
            |----2.txt

        |----plagiarism01           //folder containing plagiarized files
            |----1.txt
            |----2.txt
        .
        .
        .
        |----plagiarism07           
            |----1.txt
            |----2.txt
## 3. How to run the project?
    Run: `make FILE1="src_file_path" "other_file_path" run` command to check plagiarism between two files
    Run: `make test` to run test files in plagiarized and okay directory

#### Example run command:
make FILE1="../data/okay01/1.txt" FILE2="../data/okay01/2.txt" run