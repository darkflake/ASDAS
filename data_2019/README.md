# ASDAS
Automated Satellite Data Analysis System

### MetaData
* Satellite : [Sentinel 2 MSI - Level 2A](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR)
* Temporal Resolution : 5th Jan, 2019 to 31st Dec, 2019 - 5 day interval. [Total 73 per class]
* Spatial Resolution : 
  * Band 2 : Blue - 10m
  * Band 3 : Green - 10m
  * Band 4 : Red - 10m
  * Band 8 : NIR - 10m
  * Band 11 : SWIR - 20m ( resampled to 10m)
* [Indices](https://www.harrisgeospatial.com/docs/BackgroundOtherIndices.html) :
  * NDVI [(Normalized Difference Vegetation Index)]
  * NDWI [(Normalized Difference Water Index)]
  * NDBI [(Normalized Difference Built-up Index)]
* Data Points count :
  * Forests : 723
  * Water : 1266
  * Agriculture : 738
  * BarrenLand : 1130
  * Infrastructe : 810
* Platform : [Google Earth Engine](https://code.earthengine.google.com/?scriptPath=users%2Fshubhamverma3542_gis%2Fgis%3Adata_for_dtw)

---

> This module contains data collected from Sentinel 2 MSI satellite constellation. The data is stored into `.csv` format. The data is initially split class-wise. Further, we have 73 images per class, covering selected geometry and 5 bands mentioned in _spatial resolution_ above. CSVs for differend bands and indices are generated from this data. The indexes-csv files undergo the pre-processing pipeline.


> The Pickled Folder contains `.dat` files which store the _generalized curve_ for every index and class to be used for DTW algorithm.

---
