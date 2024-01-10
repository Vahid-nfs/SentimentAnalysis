import speech_recognition as sr
import NeuralNetwork
import LexicalAnalysis
from nltk.stem import WordNetLemmatizer
import re
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import pandas
import operator
import numpy as np
import nltk


import sys ,os
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtWidgets import QMainWindow ,QPushButton
from PyQt5.QtWidgets import QWidget 
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit, QTextEdit
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog ,QComboBox
from PyQt5.QtGui import QIcon ,QPixmap
from PyQt5 import QtGui, QtCore
import time




App = QApplication(sys.argv)


nltk.download('wordnet')
nltk.download('omw-1.4')

        

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(240,200)
        
        self.r = sr.Recognizer()
        # self.lexical = LexicalAnalysis.LexicalAnalysis()
        self.mainWindow()
        self.running = False
        self.text = ""
        self.text_sequence = None

        self.stemmer = WordNetLemmatizer()

        df = pandas.read_csv("%_by_Emo_Full_Data_data (1).csv")

        df['Tweet'] = df['Tweet'].apply(self.clean)

        MAX_NB_WORDS = 50000
        # Max number of words in each tweet.
        self.MAX_SEQUENCE_LENGTH = 250
        self.tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
        self.tokenizer.fit_on_texts(df['Tweet'].values)
        # Integer replacement
        X = self.tokenizer.texts_to_sequences(df['Tweet'].values)

        X = pad_sequences(X, maxlen=self.MAX_SEQUENCE_LENGTH)
        # Gets categorical values for the labels
        Y = pandas.get_dummies(df['Emotion']).values

        self.neuralNetwork = NeuralNetwork.NeuralNetwork(X.shape[1], 4)
        self.neuralNetwork.fit(X, Y)

    def clean(self, tweet):

        # Use this to remove hashtags since they can become nonsense words
        # trimmed_tweet = re.sub(r'(\s)#\w+', r'\1', tweet)

        # Remove all the special characters
        trimmed_tweet = re.sub(r'\W', ' ', tweet)

        # remove all single characters
        trimmed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', trimmed_tweet)

        # Remove single characters from the start
        trimmed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', trimmed_tweet)

        # Substituting multiple spaces with single space
        trimmed_tweet = re.sub(r'\s+', ' ', trimmed_tweet, flags=re.I)

        # Removes numbers
        trimmed_tweet = ''.join([i for i in trimmed_tweet if not i.isdigit()])

        # # Removing prefixed 'b'
        # trimmed_tweet = re.sub(r'^b\s+', '', trimmed_tweet)

        # Converting to Lowercase
        trimmed_tweet = trimmed_tweet.lower()

        # Lemmatization
        trimmed_tweet = trimmed_tweet.split()
        trimmed_tweet = [self.stemmer.lemmatize(word) for word in trimmed_tweet]
        trimmed_tweet = ' '.join(trimmed_tweet)
        return trimmed_tweet

    def mainWindow(self):
        btn1=QPushButton(self,text="talk")
        btn1.setGeometry(0, 10, 240, 80)


        def btn1_action():
            new_window=QMainWindow(parent=self)
            new_window.setFixedSize(480,340)
        

            new_lbl1=QLabel(text="Did i get it right ?",parent=new_window)
            new_lbl1.setGeometry(10,200,200,40)
            
            self.btn_record=QPushButton(new_window,text= "Record")
            self.btn_record.setGeometry(0, 115 , 480, 100)
            

            
            def record_action():
                self.btn_record.setText("recording ...")
                self.text = ""
                self.text_sequence = None
                self.start_capture()
            self.btn_record.clicked.connect(record_action)
                
            
            self.txtbox=QTextEdit(parent=new_window)
            self.txtbox.setDisabled(True)
            self.txtbox.setGeometry(5,10,470,100)
            
            new_btn1=QPushButton(new_window,text="Yes")
            new_btn1.setGeometry(0, 230 , 220, 100)
            
            def process_action():
                
                self.result_win=QMainWindow(new_window)
                self.result_win.setFixedSize(200,300)
                
                
                result_btn1=QPushButton(parent=self.result_win,text= "Try Again")
                result_btn1.setGeometry(0, 220, 100, 80)
                result_btn1.clicked.connect(lambda : self.result_win.close())
                
                result_btn2=QPushButton(parent=self.result_win,text= "Exit")
                result_btn2.setGeometry(100, 220, 100, 80)    
                result_btn2.clicked.connect(lambda : new_window.close())
                result_btn2.clicked.connect(lambda : self.result_win.close())
                
                self.emotional_label = QLabel(self.result_win)
                self.emotional_label.setGeometry(10, 10, 190, 190) 


                self.result_txtbox=QLabel(text="Sorry, I did not get that",parent=self.result_win)
                self.result_txtbox.setGeometry(10, 190, 180, 30)   
                self.process()
                
                self.result_win.show()
            new_btn1.clicked.connect(process_action)
            
            
            
            
            new_btn2=QPushButton(new_window,text="Try Again")
            new_btn2.setGeometry(260, 230 , 220, 100)
            new_btn2.clicked.connect(record_action)
            
            new_window.show()
        btn1.clicked.connect(btn1_action)
        
        
        btn2=QPushButton(self,text="Quit")
        btn2.setGeometry(0,100, 240, 80)
        btn2.clicked.connect(lambda : self.close())
        


    def start_capture(self):
        self.txtbox.setText("Listening ... ")
        with sr.Microphone() as source:
            self.audio_text = self.r.listen(source)
            self.btn_record.setText("Record")
            try:
                self.text = self.r.recognize_google(self.audio_text)
                self.txtbox.setText(self.text)
                self.check_value=True

            except:
                self.txtbox.setText("Sorry, I did not get that")
                self.check_value=False

    # #         # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling


    def process(self):
        

            # using google speech recognition
        
        img_dict={"confuse":"confuse.jpeg",
                  "sadness":"sadness.jpeg",
                  "anger":"anger.jpeg",
                  "joy":"joy.png",
                  "fear":"fear.png"}
        if self.check_value:
            lst = []
            lst.append(self.text)
            self.text_sequence = self.tokenizer.texts_to_sequences(lst)
            self.text_sequence = pad_sequences(self.text_sequence, self.MAX_SEQUENCE_LENGTH)
            results = self.neuralNetwork.predict(self.text_sequence)
            indexes = ""

            # results = model.predict(X_test)
            for prediction in results:
                max_percent = max(prediction)
                indexes = str(prediction.tolist().index(max_percent))
            if indexes == '0':
                print("anger")
                indexes = "anger"
            elif indexes == "1":
                print("fear")
                indexes = "fear"
            elif indexes == "2":
                print("joy")
                indexes = "joy"
            else:
                print("sadness")
                indexes = "sadness"
                
      
            print("Text: " + self.text)
            print(indexes)
            self.result_txtbox.setText(indexes)

            self.emotional_pixmap = QPixmap(f'./image/{img_dict[indexes]}')
            self.emotional_pixmap=self.emotional_pixmap.scaled(180, 180, QtCore.Qt.KeepAspectRatio)
            self.emotional_label.setPixmap(self.emotional_pixmap)
            
            
            # colours = self.lexical_analysis(self.text)
            # words = self.text.split(" ")



            # for num in range(len(words)):
            #     word = words[num]
            #     offset = "+%dc" % len(word)
                # pos_start = self.text_field.search(word, '1.0', tk.END)

            #     while pos_start:
            #         pos_end = pos_start + offset
            #         self.text_field.tag_add(colours[num]+"_tag", pos_start, pos_end)
            #         pos_start = self.text_field.search(word, pos_end, tk.END)

            # self.text_field.insert(tk.END, "\n" + indexes)
        else:
            pass
            self.result_txtbox.setText("Sorry, I did not get that")
            
            self.emotional_pixmap = QPixmap(f"./image/{img_dict['confuse']}")
            self.emotional_pixmap=self.emotional_pixmap.scaled(180, 180, QtCore.Qt.KeepAspectRatio)
            self.emotional_label.setPixmap(self.emotional_pixmap)


    def lexical_analysis(self, sentence):
        sentence = sentence.split(" ")
        lst = list()
        for word in sentence:
            values = self.lexical.find_sentiment(word)
            max_value = max(values.items(), key=operator.itemgetter(1))[0]
            print(values)
            print(max_value)
            if values[max_value] != 0:
                if max_value == "fear":
                    lst.append("blue")
                elif max_value == "anger":
                    lst.append("red")
                elif max_value == "sadness":
                    lst.append("yellow")
                elif max_value == "joy":
                    lst.append("green")
            else:
                lst.append("black")
            print(lst)
        return lst



win = Application()
win.show()
sys.exit(App.exec())














