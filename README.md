# musicBERT

### A Classifier that tells you in which decade a song was written, based on the contents of its lyrics

#### Developed by Elías Saravia & Casey McGonigle

## Workflow

### song_lyrics.py
This .py script scrapes the titles of all Billboard Hot 100 songs since 1960 from Wikipedia then accesses the Genius Lyrics API to get the lyrics for all 6200 of those songs. It stores that data in **billboard_song_lyics.csv**

### DataCreation2.ipynb
This .ipynb pulls in data from the **billboard_song_lyics.csv** and removes all the "bad" data (ie. Nones, songs with the wrong lyrics, etc.) It also ensures that all the artist names are correct & visualizes the data to ensure it fits what we expect & there aren't any horribly under-represented years or decades. Finally, it outputs the remaining ~3,500 songs to **good_lyrics_data.csv**

### Baselines.ipynb
This .ipynb pulls in our cleaned data from **good_lyrics_data.csv** and further prepares it for NLP -- performing tokenization, creating embeddings, etc. Then we run 3 basic models as baselines upon which we'd like to see improvement in our final BERT-based model.

### BERT_Fine-tuning.ipynb
This .ipynb pulls in our cleaned data from **good_lyrics_data.csv** and further prepares it for BERT -- using BERT's tokenizer to prepare the text for the BERT Model. Then, we train the model & look at results against validation & eventually test data.
