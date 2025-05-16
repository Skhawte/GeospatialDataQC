# Geospatial QC and Metadata Scripts
This repository contains a collection of Python scripts designed to assist with geospatial data quality control and metadata extraction. The scripts leverage libraries such as `arcpy`, `GDAL`, `pandas`, and `openpyxl` to automate common tasks in geospatial workflows.
---
## Scripts Included
### 1. **Featureclass_Attributetable_QC_v.1.py**
- Extracts attribute tables from shapefiles.
- Converts them to Excel.
- Highlights empty cells in red.
### 2. **QC_check_xml_medin_v.1.py**
- Parses ISO-compliant XML metadata.
- Extracts key elements (title, abstract, bounding box, contact info, etc.).
- Flags incomplete rows and highlights missing fields.
### 3. **QC_raster_properties_v.1.py**
- Extracts raster metadata using `gdal`.
- Outputs pixel size, extent, projection, and band info to Excel.
### 4. **raster_vs_ascii.py**
- Performs pixel/row count validation between `.tif` raster files and ASCII files (e.g., `.xyz`).
- Logs mismatches for quality control.
---
## Setup
### Prerequisites
Ensure the following Python packages are installed:
```bash
pip install pandas openpyxl lxml
