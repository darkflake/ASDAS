# Import the Earth Engine Python Packages
import ee
import ee.mapclient

ee.Initialize()

# Get a download URL for an image.
image = ee.Image('COPERNICUS/S2_SR/20191007T052711_20191007T053002_T43QCA')
path = image.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
})
image_b2 = image.select('B1')
print(image_b2.projection())