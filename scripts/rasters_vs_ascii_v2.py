import os
from osgeo import gdal
import pandas as pd
raster_folder = r"P:\PJ00361 - INEOS Pegasus West\84 Data QC\From OG\PJ00361_Pegasus_West_Geophy_Draft_ Deliverables\500_2D_Seismic\507_2DUHR_Isopach\CL\tBSF\VEG"
ascii_folder = r"P:\PJ00361 - INEOS Pegasus West\84 Data QC\From OG\PJ00361_Pegasus_West_Geophy_Draft_ Deliverables\500_2D_Seismic\507_2DUHR_Isopach\CL\tBSF\ASCII"
output_file = r"P:\PJ00361 - INEOS Pegasus West\87 GIS\7_Deliverable Prep\QC\507_2DUHR_Isopach_cl_tBSF.txt"
def count_valid_raster_pixels(raster_path):
   """Count valid raster pixels ignoring NoData value."""
   try:
       raster = gdal.Open(raster_path)
       if raster is None:
           raise RuntimeError(f"Could not open raster: {raster_path}")
       band = raster.GetRasterBand(1)
       nodata_value = band.GetNoDataValue()
       array = band.ReadAsArray()
       valid_pixels = (array != nodata_value).sum() if nodata_value is not None else array.size
       return valid_pixels
   except Exception as e:
       print(f"Error processing raster file '{raster_path}': {e}")
       return None
def count_valid_rows_in_ascii(ascii_path):
   """Count valid rows in an ASCII file (.xyz, .xyt, .cut, .dat, .txt)."""
   try:
       valid_rows = 0
       with open(ascii_path, 'r') as file:
           for line in file:
               line = line.strip()
               if ',' in line:
                   parts = line.split(',')
               else:
                   parts = line.split()
               if len(parts) == 3:
                   try:
                       float(parts[2])  # Check if Z is a valid float
                       valid_rows += 1
                   except ValueError:
                       continue
       return valid_rows
   except Exception as e:
       print(f"Error processing ASCII file '{ascii_path}': {e}")
       return None
def batch_qc_check(raster_folder, ascii_folder, output_file):
   """Perform QC check and log results."""
   results = []
   # Include .txt now
   valid_ascii_exts = (".xyz", ".xyt", ".cut", ".dat", ".txt")
   ascii_dict = {
       file: os.path.join(ascii_folder, file)
       for file in os.listdir(ascii_folder)
       if file.endswith(valid_ascii_exts)
   }
   for raster_file in os.listdir(raster_folder):
       if raster_file.endswith(('.tif', '.tiff')):
           raster_path = os.path.join(raster_folder, raster_file)
           ascii_names = [
               raster_file.replace(ext_r, ext_a)
               for ext_r in ['.tif', '.tiff']
               for ext_a in valid_ascii_exts
           ]
           matching_file = next((ascii_dict[name] for name in ascii_names if name in ascii_dict), None)
           if matching_file:
               raster_count = count_valid_raster_pixels(raster_path)
               ascii_count = count_valid_rows_in_ascii(matching_file)
               if raster_count is None or ascii_count is None:
                   result = f"Skipping QC for pair: {raster_file}, {matching_file} due to errors.\n"
               else:
                   qc_pass = raster_count == ascii_count
                   result = (
                       f"Raster: {raster_file}\n"
                       f"ASCII File: {matching_file}\n"
                       f"Raster Valid Pixels: {raster_count}\n"
                       f"ASCII Valid Rows: {ascii_count}\n"
                       f"QC Passed: {qc_pass}\n\n"
                   )
           else:
               result = f"Raster: {raster_file}\nMatching ASCII file not found in {ascii_folder}\n\n"
           print(result)
           results.append(result)
   with open(output_file, 'w') as f:
       f.writelines(results)
# Run the QC check
batch_qc_check(raster_folder, ascii_folder, output_file)