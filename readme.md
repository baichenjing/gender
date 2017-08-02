# Scholar Gender Prediction

A simple scholar gender predictor. To run an example demo, make sure you have access to Google, and simply run:

```Bash
pip3 install -r pip-req.txt
python3 prediction.py
```

We incorporate several classifiers here:

* Google

  We extract features from the first Google search page of the scholar, with which we train a SVM classifer for prediction. A pre-trained model is provided in *classifier/model_page.pk* as a pickle file. Find more details in our paper: [Web User Profiling Using Data Redundancy](http://keg.cs.tsinghua.edu.cn/jietang/publications/ASONAM16-Gu-et-al-web-user-profiling.pdf).

* Name

  The most widely used conventional method of gender prediction. A name-gender dictionary is generated from historical data.  We then use the new coming name to query this dictionary, and directly return the result if we find a match. If the queried name does not exist in the dictionary, the classifer output 'UNKNOWN'.

* Face

  Download the image of the target scholar from Google Image, and leverage face recognition techniques (e.g. online services provided by Face++) to get gender information. Return 'UNKNOWN' if no valid image is found. For security reasons, we hide the face recognition code. You are welcomed to use any open service or local code to complete this part.

* Vote

  A simple majority voting emsembler. We ignore any classifier who returns 'UNKNOWN'.

Enjoy, and drop me an issue if you come across any problems.

