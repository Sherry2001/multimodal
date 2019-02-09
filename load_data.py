#Purpose:
# - Collect image embeddings in one txt file, convert to Magnitude in command line 
# - Create the training set (x_train, y_train)



'''
Arg vecs: 
avg or not (default = don't average?) 
folders /data1/minh/data
data_path /data1/minh/multimodal/img_embedding.txt
'''




import numpy as np
import pickle
import pandas as pd 
import os
#from pymagnitude import *


#create one image embedding for each word by average pooling all image feature vectors
#@save img_embedding: a numpy array of image embeddings
def create_image_embedding_avg():
    # read the files that contain words and their image embeddings
    # TODO: handle duplicates or not (maybe Magnitude will eventually handle this? 

    folders = os.listdir('/data1/minh/data')
    for f in folders:
        print("Folder name: {}".format(f))
        words = pd.read_csv('/data1/minh/data/'+f, sep=' ', header=None).values
        print("Done loading from pandas")
        
        start = 0
        for i in range(words.shape[0]-1):

            # only process English words, which start with 'row'
            if words[i][0] != words[i+1][0]:
                end = i+1
                data_path = '/home/paynesa/testold'
                img_embedding = words[start:end,1:]

                # average pooling to create one single image embedding
                average_embedding = img_embedding.sum(axis=0) / img_embedding.shape[0]
                average_embedding = np.insert(average_embedding, 0, words[i][0])

                # save all embeddings to txt, convert txt to magnitude in cmd line 
                with open(data_path, 'a') as f:
                    np.savetxt(f, average_embedding.reshape(1, average_embedding.shape[0]), fmt="%s")
                start = i+1
            
            if 'column-' in words[i+1][0]:
                print("Number of English words: {}".format(i/10))
                break
    print("Done average pooling")


def create_image_embedding():
  
  """
    create one image embedding for each word by average pooling all image feature vectors
    @save img_embedding: a numpy array of image embeddings 
    """
    # read the files that contain words and their image embeddings
    # TODO: handle duplicates or not (maybe Magnitude will eventually handle this? 
folders = os.listdir('/data1/minh/data')
for f in folders:
        print("Folder name: {}".format(f))
        words = pd.read_csv('/data1/minh/data/'+f, sep=' ', header=None).values
        print("Done loading from pandas")
        
        start = 0
        for i in range(words.shape[0]-1):
            # only process English words, which start with 'row'
            if words[i][0] != words[i+1][0]:
                end = i+1
                data_path = '/home/paynesa/t'
                img_embedding = words[start:end,1:]
                # save all embeddings to txt, convert txt to magnitude in cmd line 
                with open(data_path, 'a') as f:
                    np.savetxt(f, img_embedding, fmt="%s")
                start = i+1
            
            if 'column-' in words[i+1][0]:
                print("Number of English words: {}".format(i/10))
                break
print("Done")



'''
Arg vecs: 
avg or not (default = don't average?) 
folders /data1/minh/data
data_path /data1/minh/multimodal/img_embedding.txt
'''



def create_train_set():
    """
    create the train set (x_train, y_train)
    @return x_train, y_train
    """
    words = pd.read_csv('/data1/minh/multimodal/img_embedding.txt', sep=' ', header=None).values
    # save all words in a txt file 
    np.savetxt('/data1/minh/multimodal/words.txt', words[:,0], fmt="%s")
    word_dict = Magnitude('/data1/embeddings/pymagnitude/word.magnitude')
    img_dict = Magnitude('/data1/embeddings/pymagnitude/image.magnitude')
    
    # TODO: skip over words with all NaNs    
 
    # create a file of processed words (no annotations of translation)
    # query for processed words' embeddings
    for i in range(words.shape[0]):
        unprocessed_word = words[i][0]
        # convert word, e.g row-writings to writings 
        if "row" in words[i][0]:
            phrase = words[i][0].split('-')[1]
        if "_" in words[i][0]:
            word_list = phrase.split('_')
            word = ""
            for i in range(len(word_list)):
                word += word_list[i]
                if i < len(word_list)-1:
                    word += " "
            phrase = word 
        
        with open('/data1/minh/multimodal/words_processed.txt', 'a') as f:
            f.write("{}\n".format(phrase))
        word_embedding = word_dict.query(phrase)
        img_embedding = img_dict.query(unprocessed_word)

        # check if a word has valid image vectors 
        # valid: image vectors doesn't contain all NaNs
        # check_nan = np.isnan(img_embedding)
        # all_nan = check_nan[check_nan==True].shape[0]
        # if all_nan == img_embedding.shape[0]:
            
        # add to x_train and y_train
        with open('/data1/minh/multimodal/x_train.txt', 'a') as f:
            np.savetxt(f, word_embedding.reshape(1, word_embedding.shape[0]))
        with open('/data1/minh/multimodal/y_train.txt', 'a') as f:
            np.savetxt(f, img_embedding.reshape(1, img_embedding.shape[0]))

create_image_embedding_avg()
