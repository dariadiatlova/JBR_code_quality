Test task for the project: Code quality for online learning platforms Stepik and Hyperskill (JBR)

# Repository structure:
1. radon_script.py -- script computes several metrics from radon library for all files in a current directory and save the results to log.txt
2. log.txt -- file with the metrics output 
3. librosa_core -- directory with the files from librosa library (used as an example for Project code analysis)
 
# Results overview:
Radon is a Python tool that computes various metrics from the source code https://github.com/rubik/radon. 
Presented script is one of many ways to annalyze the project, it consists of 3 main parts:
I. Score and sort all methods in each projects by Cyclomatic Complexity (corresponds to the number of decisions a block of code contains plus 1).
II. Score and sort all files in a directory by Maintainability Index – software metric which measures how maintainable (easy to support and change) the source code is.
III. Sort all files in current directory by Cyclomatic Complexity and score them by raw metrics: 
  - rank (an assesment based on the Cyclomatic Complexity);
  - LLOC (Logical Lines of Code);
  - HV (the Halstead Volume);
  - % of LC (he percent of lines of comment).
Additional computation details on metrics could be found in radon documentation https://radon.readthedocs.io/en/latest/intro.html#cyclomatic-complexity

# How to run the script:
1. Install radon library using pip install radon or conda install -c conda-forge radon.
2. Locate the script in a directory with the files you want to score.
