
### One-hot encoding
Euclidean distance between two distinct one-hot encoded vectors, e.g. [1,0] and [0,1] is always the same. This is important! If we mapped the $i$th token to the number $i$ then euclidean distances would be different in arbitrary ways.
### BOW: Bag of words
= sum of one-hot vectors for a text
### $n$-grams
Preserve some word ordering (up to length $n$), but can have huge feature vectors if using one-hot $n$-grams
### TF-IDF
Term Frequency: $\text{tf}(t,d)$ of token $t$ in document $d$ can be:
- raw count: number of times the token appears in the document (usual choice)
- boolean: 1 if appears at least once, 0 otherwise
- normalised: $$\frac{\text{number of times token appears in document}}{\sum_{t'\in T} \text{number of times t' appears in document d}}$$
- $\log(1 + \text{raw count})$
Document Frequency: number of documents that contain the token $t$
Inverse Document Frequency:
$$\log(\frac{\text{number of documents}}{1 + \text{df}(t)})$$ or add 1 in sklearn idf
idf(t) is large when df(t) is small

- reasonable heuristic for identifying **informative** tokens, tokens that differentiate texts

### Vector Embeddings:
#### word2vec and GloVe
Train an MLP to predict surrounding words of a target word. Use embeddings as encoding of target word in downstream tasks.
#### BERT
- transformer neural net
- use word-piece tokenization
- predict target word from surrounding word (fill in the blanks)
- BERT and related transformers are probably now the baseline, but they are computationally expensive
- usually use pretrained models and then fine-tune because they take a lot of training