import pandas as pd
import warnings
from clean_names import get_clean_names
from unidecode import unidecode
import os

# Load data
tabdata_link = "https://data.humdata.org/dataset/caf116df-f984-4deb-85ca-41b349d3f313/resource/e74fd350-3728-427f-8b4c-0589dc563c87/download/phl_adminboundaries_tabulardata.xlsx"
# Ignore warning about frozen rows
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
admin_areas = pd.read_excel(tabdata_link)

# Remove unnecessary 0s
admin_areas["adm1_new"] = admin_areas["ADM1_PCODE"]
admin_areas["adm2_new"] = admin_areas["ADM1_PCODE"] + admin_areas["ADM2_PCODE"].str[-2:]
admin_areas["adm3_new"] = admin_areas["ADM1_PCODE"] + admin_areas["ADM3_PCODE"].str[-4:]
admin_areas["adm4_new"] = admin_areas["adm3_new"] + admin_areas["ADM4_PCODE"].str[-2:]

# Add columns with clean/minimal area names for matching
for i in range(1, 5):
    admin_areas["adm" + str(i) + "_clean"] = get_clean_names(admin_areas["ADM" + str(i) + "_EN"])
# print(admin_areas.head())

# Add index header
admin_areas.index.name = "index"

# Export to CSV
os.makedirs("export", exist_ok = True)
admin_areas.to_csv(os.getcwd() + "/export/" + "phl_adminareas_fixed" + ".csv")
