import os
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import re
import geopandas as gpd
import topojson as tp

# If no source and export folders exist, make them
os.makedirs("shp_source", exist_ok = True)
os.makedirs("export", exist_ok = True)

# Access shapefiles and save to folder
shapefiles_link = "https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/12457689-6a86-4474-8032-5ca9464d38a8/download/phl_adm_psa_namria_20231106_shp.zip"
with urlopen(shapefiles_link) as z:
    with ZipFile(BytesIO(z.read())) as zfile:
        zfile.extractall(os.getcwd() + "/shp_source")
print("Shapefiles downloaded")

# Make list of shapefiles
shapefile_list = os.listdir(os.getcwd() + "/shp_source")
# For each admin level, find file, edit, and save
for i in range(0, 5):
    to_find = re.compile(".*adm" + str(i) + ".*shp$")
    shp_file = list(filter(to_find.match, shapefile_list))[0]
    gdf = gpd.read_file(os.getcwd() + "/shp_source/" + shp_file)
    # Remove datetime column because it just causes issues
    gdf = gdf.select_dtypes(exclude = ["datetime64"])

    # Remove unnecessary 0s
    gdf["adm0_new"] = gdf["ADM0_PCODE"]
    if i >= 1:
        gdf["adm_new"] = gdf["ADM1_PCODE"]
        if i >= 2: 
            gdf["adm2_new"] = gdf["ADM1_PCODE"] + gdf["ADM2_PCODE"].str[-2:]
            if i >= 3:
                gdf["adm3_new"] = gdf["ADM1_PCODE"] + gdf["ADM3_PCODE"].str[-4:]
                if i >= 4:
                    gdf["adm4_new"] = gdf["adm3_new"] + gdf["ADM4_PCODE"].str[-2:]
    
    # Export to Shapefile
    os.makedirs("export/shp", exist_ok = True)
    gdf.to_file(os.getcwd() + "/export/shp/" + "phl_adm" + str(i) + "_fixed" + ".shp")
    print("New admin " + str(i) + " shapefile saved")

    # Export to GeoJSON
    os.makedirs("export/geojson", exist_ok = True)
    gdf.to_file(os.getcwd() + "/export/geojson/" + "phl_adm" + str(i) + "_fixed" + ".geojson", driver = "GeoJSON")
    print("New admin " + str(i) + " GeoJSON saved")

    # # Simplify and export to JSON to use as TopoJSON in Power BI
    # # Problem: this currently makes the kernel crash
    # os.makedirs("export/topojson_simplified", exist_ok = True)
    # tp.Topology(gdf, toposimplify = .05).to_json(os.getcwd() + "/export/topojson_simplified" + "phl_adm" + str(i) + "_simple" + ".json")
    # print("Simplified TopoJSONs saved")