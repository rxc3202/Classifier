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

### Hypothesis Generation
The hypothesis in the form of an ensemble or a decision tree is output to the file named after the argument provided via the command line. The format of the file is two lines dilineated by the "`\n`" character. The first line contians the abbreviation `dt` or `ada` to specify that the next line is an encoding of a decision tree or an adaboosted forest.

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
             |---aa
                 |---nl
                 |---oo
                     |---nl
                     |---jn
                         |---nl
                         |---van
                             |---nl
                             |---uu
                                 |---en
                                 |---of
                                     |---en
                                     |---en
         |---de
             |---nl
             |---aa
                 |---nl
                 |---en
```
#### Expirimentation
The following data was taken using the full set of features on a test set (found at `etc/testing.txt`) which is a set of 20 samples. 10 are English samples and 10 are Dutch samples. 
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
| 3     |      20%      |     0%      |
| ...   |      ...      |     ...     |
| inf   |      0%       |     0%      |

### Adaboost Analysis
My adaboost ensemble was create from the same attributes listed above, therefore the ensemble consisted of 10 stumps. When training the adaboost forest, I used the same 100 sample training set found at `etc/training.txt` and used the same test set at `etc/testing.txt`. However, when classifying the testing set, the classification was incredibly poor for dutch samples and incredibly good for english ones. I belive this imbalance was caused by misweighting of the stumps in the adaboost algorithm or the features themselves.

| Language |  Correct  |
|:--------:|:---------:|
| Dutch    | 20%       |
| English  | 100%      |

The tree it generates is as follows. Each branch is listed in the order of the tuples defined in `processing.py` in this case the specification for each of this attributes is `(<attr_name>, True, False)` meaning that each child takes the form:
```
<attr_name>:(approx. <weight>)
    |---(True Branch)
    |---(False Branch)
```

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
jn:(~1.53)
    |---nl
    |---en
de:(~2.28)
    |---nl
    |---en
van:(~2.93)
    |---nl
    |---en
a:(~-0.51)
    |---en
    |---nl
en_ending:(~0.59)
    |---nl
    |---en
oo:(~2.00)
    |---nl
    |---en
of:(~0.09)
    |---en
    |---nl
```

#### Expirimentation


#### Files and Descriptions

| Filename | Function |
| -------- | -------- |
|`decisiontree.py`| This file contains the implementation of the Decision Tree based learning algorithm. Inside is a single class `DecisionTree`. |
|`adaboost.py`| This file contains the implementation of the adaboost algorithm. Inside is a single subclass of `DecisionTree` named `Adaboost`. |
|`processing.py`  | This file is for exports used within the `Adaboost` and `DecisionTree` classes. Inside users must define the attribute names, the possible values for those attributes, and the functions used to process a line of text |
|`classifier.py`  |  The running file used to start the program with the command line arguments specificed in the Lab2 writeup |


```python
def process_file(filename, training=True):
    raw_text = []
    with open(filename, 'r') as f:
        raw_text = [re.sub("[^(a-zA-Z\d\-\s)]",'', line).strip("\n ") for line in f]
    labeled_examples = []
    for example in raw_text:
        example = example.split("|")
        if training:
            labeled_examples.append(tuple([f(example[1]) for f in processing_funcs] + [example[0]]))
        else:
            labeled_examples.append(tuple([f(example[0]) for f in processing_funcs] + [None]))
    return labeled_examples
```

#### Feature Selection

Feature selection for this project used only binary attributes, even though the implementation could support mulitple values. Features were selected with the idea of character sequence frequency in mind. There were combinations of letters (and words) that were only found in one of the two languages. All these were taken after scanning pages of text to spot any features of the Dutch language as well as differences between dutch and english. The features chosen and their monikers are the following:

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

#### Removed Features
| Feature | Values | Description | Justification |
|---------|-----------|-------------|---------------------|
|`oo`| `True`/`False` | `True` if the text contains at least 1 word the subtring `"oo"`| The english language doesn't have native words with `oo`|
|`ee`|`True`/`False`| `True` if the text contains at least 1 word with the subtring `ee`|The english language doesn't have native words with `ee`|
|`gt1z`|`True`/`False`| `True` if the text contains at least 3 word with the subtring `gt1z`|The english language doesn't have native words with `gt1z`|