# Project 2 : Langauge Classifier

How To Run
==========
#### Grading
```bash
$ python3 classifier.py train etc/training.txt hypothesis.txt dt
$ python3 classifier.py predict <file> hypothesis.txt
```

#### Testing using my examples
```bash
$ python3 classifier.py train etc/training.txt hypothesis.txt dt
$ python3 classifier.py predict etc/testing.txt hypothesis.txt
```


Methodology
===========
#### Data gathering
Examples were gathered by hand using the linkes provided in the writeup. 50 lines of text were gathered from both the English and Dutch wikis creating a total training sample set of 100. The samples can include and the processing algorithm (shown below) will remove all uncessary punctuation so that only the raw words are left. This can be accessed at `etc/training.txt`. 

#### Feature Selection

Feature selection for this project used only binary attributes, even though the implementation could support mulitple values. Features were selected with the idea of character sequence frequency in mind. There were combinations of letters (and words) that were only found in one of the two languages. All these were taken after scanning pages of text to spot any features of the Dutch language as well as differences between dutch and english. The features chosen and their names are the following: 

| Feature | Values | Description | Justification |
|---------|-----------|-------------|---------------------|
|`aa`| `True`/`False` | `True` if the text contains at least 1 word the subtring `"aa"`| The english language doesn't have native words with `aa`|
|`uu`|`True`/`False`| `True` if the text contains at least 1 word with the subtring `uu`|The english language doesn't have native words with `uu`|
|`aa`| `True`/`False` | `True` if the text contains at least 1 word the subtring `"aa"`| Double `oo` is seems to be much more frequent in dutch text |
|`the`|`True`/`False`| `True` if the text contains the word `the` | The Dutch language does not use the word `the`| 
|`jn`|`True`/`False`| `True` if the text contians the a word with the subtring `jn`| The English language doesn't have any native words that have the consonant combination `jn`|
|`de`|`True`/`False`| `True` if the text contains the word `de` | The English language doesn't have the word `de`|
|`of`|`True`/`False`| `True` if the text contains the word `of` | The Dutch language doesn't have the word `of`|
|`van`|`True`/`False`| `True` if the text contains the word `van` | `van` is a very common Dutch word meaning "of" or "from" which is a frequently used word|
|`a`|`True`/`False`| `True` if the text contains the word `a` | Dutch does not have the word `a`|
|`en_ending`|`True`/`False`| `True` if the text has a word ending in `en`| A common conjucation of verbs in Dutch make words have the ending `-en`|
|`ee`|`True`/`False`| `True` if the text contains at least 1 word with the subtring `ee`|The english language doesn't have native words with `ee`|
|`oo`| `True`/`False` | `True` if the text contains at least 1 word the subtring `"oo"`| There are a lot of dutch words with `oo`|

For the most part, these were shared between the two algorithms, however after testing some may have been removed. This is just the full set of features that were used between the two algorithms

### Hypothesis Generation
The hypothesis in the form of an ensemble or a decision tree is output to the file named after the argument provided via the command line. The format of the file is two lines dilineated by the "`\n`" character. The first line contians the abbreviation `dt` or `ada` to specify that the next line is an encoding of a decision tree or an adaboosted forest. There is no new line at the end of the tree structure. Just the  `EOF`.

```
dt
(4, 'nl', (8, (2, 'en', (7, 'en', (0, 'nl', (1, 'nl', (3, 'nl', (6, 'nl', (5, 'nl', 'nl'))))))), (0, 'nl', 'en')))
```
> This is the encoding of the of best decision tree my features have produced

### Decision Tree Analysis
The decision tree created using the features I chose does classification at nearly 100% correct with a training set of 100 samples (described above) and then tested using a set of 20 examples for testing. The training set and the testing set (found at `etc/training.txt` and `etc/testing.txt`) have no overlapping samples.

| Language |  Correct  |
|:--------:|:---------:|
| Dutch    | 100%      |
| English  | 100%      |

The tree it generates is as follows. Each branch is listed in the order of the tuples defined in `processing.py` in this case the specification for each of this attributes is `(<attr_name>, True, False)` meaning that each child takes the form:
```
<attr_name>
    |---(True Branch)
    |---(False Branch)
```

##### Best Decision Tree Generated
```
 the
 |---en
 |---a
     |---en
     |---en_ending
         |---de
             |---nl
             |---ee
                 |---nl
                 |---aa
                     |---nl
                     |---van
                         |---nl
                         |---en
         |---de
             |---nl
             |---aa
                 |---nl
                 |---en
```
#### Expirimentation
The following data was taken using the full set of features on a test set (found at `etc/testing.txt`) which is a set of 50 samples. 25 are English samples and 25 are Dutch samples. 
The first approach to the features used in the decision tree was to analyze the unique combinations of letters in the words. At first, these were the only types of features I included in the feature set and it comprised of features such as ("aa", "oo", "ee", "uu", "jn", ends in "en")

| Depth | English Error | Dutch Error |
|:-----:|:-------------:|:-----------:|
| 1     |      0%       |     100%    |
| 2     |      0%       |     30%     |
| 3     |      40%      |     10%     |
| 4     |      40%      |     10%     |
| ...   |      ...      |     ...     |
| inf   |      40%      |     10%     |

This only allowed the decision tree to to reach a very poor classification rate. After trying to come up with more features, this eventually led nowhere as well and the error rate never each an acceptable level.

As you can see, after deciding to look at letter combination frequency (i.e "oo", "aa", "uu") as well as word frequency (i.e "the" "a", "of", etc), the error rate drops off much faster. The following error table resulted in from taking some attributes out (see Removed Attributes Section) and adding the frequent word features.

| Depth | English Error | Dutch Error |
|:-----:|:-------------:|:-----------:|
| 1     |       0%      |     100%    |
| 2     |      20%      |     0%      |
| 3     |      4%       |     0%      |
| 4     |      4%       |     0%      |
| 5     |      0%       |     8%      |
| 5     |      0%       |     0%      |
| ...   |      ...      |     ...     |
| inf   |      0%       |     0%      |

With the best set of features in place, I turned to sample size testing to see at what point my tree could reach near perfect classification. The following tests were run by taking chunks of the `etc/training.txt` file that increase by 10. So the first test would only have 10 examples, then 20, etc until the full sample set of 100 was used. **_The tree depth algorithm ran to completion, creating different depth trees since more examples mean more entropy to account for._**

| Sample Size| English Error | Dutch Error |
|:-----:|:-------------:|:-----------:|
| 10     |      0%      |     24%     |
| 20     |      0%      |     8%      |
| 30     |      0%      |     8%      |
| 40     |      0%      |     8%      |
| 50     |      0%      |     8%      |
| 60     |      0%      |     0%      |
| 70     |      0%      |     0%      |
| 80     |      0%      |     4%    |
| 90     |      0%      |     0%      |
| 100    |      0%      |     0%      |


### Adaboost Analysis
My adaboost ensemble was create from the same attributes listed above, therefore the ensemble consisted of 11 stumps. When training the adaboost forest, I used the same 100 sample training set found at `etc/training.txt` and used the same test set at `etc/testing.txt`. However, when classifying the testing set, the classification was incredibly poor for dutch samples and incredibly good for english ones. I belive this imbalance was caused by misweighting of the stumps in the adaboost algorithm or the features themselves.

| Language |  Correct  |
|:--------:|:---------:|
| Dutch    | 64%       |
| English  | 100%      |

The tree it generates is as follows. Each branch is listed in the order of the tuples defined in `processing.py` in this case the specification for each of this attributes is `(<attr_name>, True, False)` meaning that each child takes the form:
```
<attr_name>:(approx. <weight>)
    |---(True Branch)
    |---(False Branch)
```

#### Initial Adaboost Weights
```
de:(~1.20)
    |---nl
    |---en
van:(~1.05)
    |---nl
    |---en
a:(~0.28)
    |---en
    |---nl
en_ending:(~0.89)
    |---nl
    |---en
oo:(~0.75)
    |---nl
    |---en
of:(~0.27)
    |---en
    |---nl
ee:(~0.73)
    |---nl
    |---en
aa:(~2.01)
    |---nl
    |---en
uu:(~0.44)
    |---nl
    |---en
the:(~0.89)
    |---en
    |---nl
jn:(~0.97)
    |---nl
    |---en
```

## Expirimentation
The main experimentation I did with adabosst was the order in which the stumps were introduced to the algorithm. Since the first stumps output will affect the error rates of the next and so on, the order of the stumps will affect the weights. However, since there are too many combinations, I only rotated the order in which the stumps were traversed. (i.e [attr1, attr2, attr3, attr4] ---> [attr4, attr1, attr2, attr3] --->[attr4, attr1, attr2, attr3]). The originial order of the feature stumps are :

| Rotation | Order | English Error | Dutch Error |
|:--------:|:-------------:|:-----------:|:----------:|
| 0 (original)      |`['aa', 'uu', 'the', 'jn', 'de', 'van', 'a', 'en_ending', 'oo', 'of', 'ee']`|     0%      |     36%      |
| 1       |`['ee', 'aa', 'uu', 'the', 'jn', 'de', 'van', 'a', 'en_ending', 'oo', 'of']`|     0%      |     52%     |
| 2       |`['of', 'ee', 'aa', 'uu', 'the', 'jn', 'de', 'van', 'a', 'en_ending', 'oo']`|     0%      |     36%      |
| 3       |`['oo', 'of', 'ee', 'aa', 'uu', 'the', 'jn', 'de', 'van', 'a', 'en_ending']`|     0%      |     40%      |
| 4       |`['en_ending', 'oo', 'of', 'ee', 'aa', 'uu', 'the', 'jn', 'de', 'van', 'a']`|     0%      |     40%      |
| 5       |`['a', 'en_ending', 'oo', 'of', 'ee', 'aa', 'uu', 'the', 'jn', 'de', 'van']`|     0%      |     24%      |
| 6       |`['van', 'a', 'en_ending', 'oo', 'of', 'ee', 'aa', 'uu', 'the', 'jn', 'de']`|     0%      |     20%      |
| 7       |`['de', 'van', 'a', 'en_ending', 'oo', 'of', 'ee', 'aa', 'uu', 'the', 'jn']`|     0%      |     32%      |
| 8       |`['jn', 'de', 'van', 'a', 'en_ending', 'oo', 'of', 'ee', 'aa', 'uu', 'the']`|     0%      |     24%    |
| 9       |`['uu', 'the', 'jn', 'de', 'van', 'a', 'en_ending', 'oo', 'of', 'ee', 'aa']`|     0%      |     28%      |

As you can see by the testing done here, it shows that the ordering of the stumps matter since the previous ones do affect the ones that come after it. In the case of my features, it seems that they do not make good stumps since only the error rate the the Dutch is ever affected. After viewing the weights associated with the best tree, the weights indicated for `jn`, `de`, `van`,`oo` were incredibly high, meaning that they could be throwing off the algorithm becaues they were not "poor learners". After removing these strongly weighted stumps, the error rate became slightly better in total and as well as more balanced.

```
aa:(~1.09)
    |---nl
    |---en
uu:(~0.35)
    |---nl
    |---en
the:(~0.67)
    |---en
    |---nl
a:(~-0.22)
    |---en
    |---nl
en_ending:(~0.83)
    |---nl
    |---en
of:(~0.40)
    |---en
    |---nl
ee:(~1.19)
    |---nl
    |---en
```
| Language |  Correct  |
|:--------:|:---------:|
| Dutch    | 92%       |
| English  | 92%      |

#### Files and Descriptions

| Filename | Function |
| -------- | -------- |
|`decisiontree.py`| This file contains the implementation of the Decision Tree based learning algorithm. Inside is a single class `DecisionTree`. |
|`adaboost.py`| This file contains the implementation of the adaboost algorithm. Inside is a single subclass of `DecisionTree` named `Adaboost`. |
|`processing.py`  | This file is for exports used within the `Adaboost` and `DecisionTree` classes. Inside users must define the attribute names, the possible values for those attributes, and the functions used to process a line of text |
|`classifier.py`  |  The running file used to start the program with the command line arguments specificed in the Lab2 writeup |
| `etc/test_dt.py` |  A helper program that allowed me to do depth and sample size testing for testing decision tree effectiveness|
| `etc/test_ada.py` |  A helper program that allowed me to test feature stump order for adaboost|
| `etc/test_processing.py` | a copy of the `processing.py` file that allowed me to test different attributes without messing up the original |

#### File processing Function
```python
def process_file(filename, training=True):
    raw_text = []
    with open(filename, 'r') as f:
        raw_text = [re.sub("[^(a-zA-Z\d\-\s)]",'', line).strip("\n ") for line in f]
    labeled_examples = []
    for example in raw_text:
        example = example.split("|")
        if training:
            # For each attribute, use its function to classify that feature as true or false for that example
            # Example{f1(text), f2(text), f3(text), ...} ->Example{True, False, False, ...}
            labeled_examples.append(tuple([ f(example[1]) for f in processing_funcs] + [example[0]]))
        else:
            labeled_examples.append(tuple([f(example[0]) for f in processing_funcs] + [None]))
    return labeled_examples
```


#### Removed Features
| Feature | Values | Description | Justification |
|---------|-----------|-------------|---------------------|
|`gt1z`|`True`/`False`| `True` if the text contains at least 3 word with the subtring `gt1z`|The english language doesn't have a lot native words with the letter `z` so the more z's the better the chance it is dutch|