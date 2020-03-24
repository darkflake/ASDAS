# ASDAS
Automated Satellite Data Analysis System

### Pre - processing Pipeline
* Combining class-wise data into Bandwise CSV files - [Blue, Green, Red, NIR, SWIR, SCL] and indices - [[NDVI, NDWI, NDBI]](https://www.linkedin.com/pulse/ndvi-ndbi-ndwi-calculation-using-landsat-7-8-tek-bahadur-kshetri)
* Handline Missing Values 
* Atmospheric correction : Cloud detection and masking.
* Linear Interpolation to overcome temporary cloud - affected dates in the temporal analysis
* [Savitsky - Golay Filter](http://www.statistics4u.com/fundstat_eng/cc_filter_savgolay.html) to smoothen the temporal curve and manage the erratic flow.

---

The basic pre-processing pipleline runs through the single `main.py` file, with a driver function `preprocess()`. 
Fully preprocessed files are saved in the data storage directories to be accessed by the processing modules.

---
