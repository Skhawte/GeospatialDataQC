
import os
from osgeo import gdal
import pandas as pd

# Function to extract metadata and properties from a raster file
def extract_raster_info(file_path):
   try:
       dataset = gdal.Open(file_path)
       if dataset is None:
           print(f"Unable to open file: {file_path}")
           return None
       geotransform=dataset.GetGeoTransform()
       pixel_width=geotransform[1]
       pixel_height=abs(geotransform[5])

       metadata = {
           "File Path": file_path,
           "Driver": dataset.GetDriver().LongName,
           "Raster extent-x": dataset.RasterXSize,
           "Raster extent-y": dataset.RasterYSize,
           "Number of Bands": dataset.RasterCount,
           "Data Type": gdal.GetDataTypeName(dataset.GetRasterBand(1).DataType),
           "Projection": dataset.GetProjection(),
           "NoData Value": dataset.GetRasterBand(1).GetNoDataValue(),
           "Pixel width": pixel_width,
           "Pixel height": pixel_height




       }
       return metadata
   except Exception as e:
       print(f"Error processing file {file_path}: {str(e)}")
       return None
# List of raster file paths
folder_path = r"P:\PJ00356 - Inch Cape\356a Survey\83 Geophysics\fromOG\Final Deliverables\ECR\100_MBES\103 - MBES Density\TIF-VEG"
tif_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".tif")]

# Create an empty list to store the metadata of each raster file
all_data = []
# Process each raster file
for tif_file in tif_files:
   data = extract_raster_info(tif_file)
   all_data.append(data)
# Create a DataFrame from the extracted data
df = pd.DataFrame(all_data)
# Save the DataFrame to an Excel file
output_file = r"P:\PJ00356 - Inch Cape\356a Survey\87 GIS\7_Deliverable Prep\QC\MBES_density_veg.xlsx"

df.to_excel(output_file, index=False)
print(f"Raster properties has been saved to {output_file}")
