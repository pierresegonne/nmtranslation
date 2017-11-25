"""
Create a dataset from txt file, serializes it
"""
import codecs
from collections import Counter
import _pickle as pickle
import operator

def read_sentence(filePath):
    sentences = []

    with codecs.open(filePath, 'rb', encoding='UTF-8') as reader:
        for sentence in reader:
            sentences.append(sentence)

    return sentences

def create_dataset(fr_sentences,da_sentences,max_words = 30000,max_sentence_length=15):
    # dictionary with count of the appearances of words
    # str = "0000000this is string example....wow!!!0000000";
    # print
    # str.strip('0')
    fr_vocab_dic = Counter(word.strip(',." ;:-)(][?!').lower() for sentence in fr_sentences for word in sentence.split())
    da_vocab_dic = Counter(word.strip(',." ;:-)(][?!').lower() for sentence in da_sentences for word in sentence.split())

    # map of words, sorted by desc appearances
    # print(list(map(lambda x: x[0], sorted(fr_vocab_dic.items(), key = lambda x: x[1], reverse=True))))
    fr_vocab = list(map(lambda x: x[0], sorted(fr_vocab_dic.items(), key = lambda x: x[1], reverse=True)))
    da_vocab = list(map(lambda x: x[0], sorted(da_vocab_dic.items(), key = lambda x: x[1], reverse=True)))

    # keep the most frequent words
    fr_vocab = fr_vocab[:max_words]
    da_vocab = da_vocab[:max_words]
    print(fr_vocab)
    print(da_vocab)

    #word 2 index
    #TODO understand this |=| padding
    start_index = 2
    fr_word2ind_dic = dict([(word, start_index + ind) for ind, word in enumerate(fr_vocab)])
    fr_word2ind_dic['<ukn>'] = 0
    fr_word2ind_dic['<pad>'] = 1
    print(fr_word2ind_dic)

    # fr_ind2word_dic = dict([(word2ind[1],word2ind[0]) for ind, word2ind in enumerate(fr_word2ind_dic.items())])
    fr_ind2word_dic = dict([(ind,word) for word, ind in fr_word2ind_dic.items()])

    print(fr_ind2word_dic)

    start_index = 4
    da_word2ind_dic = dict([(word, start_index + ind) for ind, word in enumerate(da_vocab)])
    da_word2ind_dic['<ukn>'] = 0
    da_word2ind_dic['<go>'] = 1
    da_word2ind_dic['<eos>'] = 2
    da_word2ind_dic['<pad>'] = 3

    da_ind2word_dic = dict([(ind,word) for word, ind in da_word2ind_dic.items()])

    #x fr, source, list of indices of sentences words
    #y, da, target
    x = [[fr_word2ind_dic.get(word.strip(',." ;:-)(][?!'), 0) for word in sentence.split()] for sentence in fr_sentences]
    y = [[da_word2ind_dic.get(word.strip(',." ;:-)(][?!'), 0) for word in sentence.split()] for sentence in da_sentences]

    print(x,y)
    # filtered sentences, length comparison and overall length
    X = []
    Y = []
    for ind in range(len(x)):
        nx = len(x[ind])
        ny = len(y[ind])
        n = max(nx,ny)
        if abs(nx-ny) < 0.3*n :
            if nx<=max_sentence_length and ny<=max_sentence_length :
                X.append(x[ind])
                Y.append(y[ind])

    return X, Y, fr_word2ind_dic, da_word2ind_dic, fr_ind2word_dic, da_ind2word_dic, fr_vocab, da_vocab







def save_dataset(filePath, dataset):

    with open(filePath, 'wb') as serializer:
        pickle.dump(dataset, serializer, -1)

def read_dataset(filePath, dataset):

    with open(filePath, 'rb') as reader:
        return pickle.load(reader)


def main():
    fr_sentences = read_sentence('./data/data.da-fr.fr')
    da_sentences = read_sentence('./data/data.da-fr.da')

    dataset = create_dataset(fr_sentences,da_sentences)

    save_dataset('./data.pkl',dataset)

if __name__ == '__main__':
    main()