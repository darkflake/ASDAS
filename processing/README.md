# ASDAS
Automated Satellite Data Analysis System

---

The main processing module of the project. Performs different algorithms for satellite data processing.

---

#### SIGNAL MATCHING ALGORITHM - Functionalities included :
* Create an _generalised_ curve from a dataset -
  > From a dataset of data points with same class label, average value of every column is calculated. This curve denotes the _general_ 
  curve for that label.
* Apply `fastDTW` to get the distance between curves -
  > This can be done between a template and a single curve or between a template and dataset of curves. In case, comparison is done between
  two single curves, the graph renders a line graph with connection between most similar points. If the dataset of curves is passed, 
  a bar plot denoting distance between every curve and template is rendered.
* Calculating _ simple threshold_ :
  > The distance calculated from applying `FastDTW` on two curves is compared with the list of distances obtained by testing dataset. 
  The percentile of that distance amongst all the distances denotes its _ simple threshold_.
* Calculating _90 percentile threshold_ :
  > Applying DTW algorithm all the training curves, and calculating the distance of top 90% nearest curves is the threshold value for 
  classifying a testing curve for that class.
* Pickler and Unpickler :
  > Using the inbulit `pickle` functionality of python, we store a dictionary with _generalised curve_ and _distances list_ of the training
  dataset for every class and every index. This results in higher speed of execution, as the algorthim need not perform the computations
  on training dataset every time.
* **Trainer** :
  > The main driver function to perform the pipeline of obtainng _generalised curve_ and _distances list_ and pickling the information.
  This function is performed one index on single class at a time.
* **Tester** :
  > The main driver function to perform the pipleline of unpickling the data and _calculating threshold_ for the test curve agains all
  the general curves available. (Currently 3 indices x 5 classes). An additional functionality of applying the technique for entire 
  training dataset is provided, which will create a labelled dataset with signal matching algorithm applied on entire training dataset.

---
