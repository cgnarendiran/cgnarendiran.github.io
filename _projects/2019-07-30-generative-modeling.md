---
layout: project
title:  Generating synthetic medical data
date:   2019-07-30
image:  images/project6/cover.png
tags:   ctcue lstm dbc dutch healthcare 
---
*On the cover: CtCue Logo; All rights reserved by CtCue B.V Nedtherlands*

One of the main challenges of working with medical data is it's strict confidential nature. In order to test software solutions on medical data outside of a hospital, one needs to create synthetic data that is representative of the original data. This internship deals with building a tool for generating realistic fake patient health records following the structure of CTcue-datamodel (an in-house created patient-centric clinical data structure containing patient demographics and related categories such as admissions, appointments, medications, measurements, etc). This tool (generative model) can be used for generating data that can be used in testing the query pipeline system at CTcue. For initial tool building and testing, we used data from Synthea - a Synthetic Patient Population Simulator which is a reference data generator for our case. This generates synthetic patient records for a given module, say Diabetes. We then have to fit the tool to work with CTcue datamodel.

Generating fake medical data is challenging because of two factors:
1. Patient health records data is discrete and rigid unlike music or images. Defining the **input data structure** for generative modelling is crucial to the successive tasks.
2. Patient records feature complex underlying relations to the disease and it’s progression, diagnosis, medication and dosage, medical tests and follow-ups. These complex relations are hoped to be learned by the adopted generative model. 

An LSTM seq2seq model was trained with tempered softmax as an autoencoder for generating synthetic medical timestamp events. Since the data is categorical and sequential, one needs to pre-process the data into a suitable input for the model. Synthea and CTcue feature different pre-processing techniques as the datamodel differs. But the blueprint remains the same which is, 
1. Loading/querying the data off the disk partially or fully 
2. Pruning the loaded data and building records by various intermediate steps (eg. adding the “Start event” and “Terminal event”) and store them as dictionaries
3. Building and storing the vocabulary of events while loading 
4. Sparse encoding the event sequence of patients records and pass them on to the model during training
5. Pre-train Gensim’s Word2Vec model and use those embeddings (optional)

**The results are not presented due to the confidential nature of the internship**
