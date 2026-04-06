# PHL_fix_admin_files
Scripts to take geographic data for the Philippines and standardise it, enabling interoperability across datasets. Originally developed for the Philippines Shelter Cluster in January/February 2026.

### Inputs:
1. OCHA admin boundaries (tabular data) available here: https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/e74fd350-3728-427f-8b4c-0589dc563c87/
2. OCHA administrative level 0-4 shapefiles available here: https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/12457689-6a86-4474-8032-5ca9464d38a8/

The scripts access these files directly from their locations on the Humanitarian Data Exchange.

### Outputs:
1. A CSV sheet with all administrative areas at admin level 4, including all intermediate admin levels, cleaned P-codes for admin levels 1-4, and cleaned/minimal admin area names for levels 1-4 that can aid in joining data when P-codes are not available and spelling is inconsistent.
2. Admin area polygons with cleaned P-codes and cleaned/minimal names; separate files for admin levels 1-4 in the following formats:
- Shapefile
- GeoJSON
- Simplified TopoJSON for use in Power BI (work in progress)
