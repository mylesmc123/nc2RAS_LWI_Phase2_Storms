from mil.army.usace.hec.vortex.io import BatchImporter
from mil.army.usace.hec.vortex.geo import WktFactory
import glob

# C:\Program Files\HEC\HEC-HMS\4.8>HEC-HMS.cmd -script "C:\jy\vortexImport\vortex_import.py"

# in_files = [r"C:\jy\vortexImport\MRMS_GaugeCorr_QPE_01H_00.00_20170102-120000.grib2"]
# variables = ['GaugeCorrQPE01H_altitude_above_msl']
# in_files = [r"C:\jy\vortexImport\tcr-20min-ISAAC_2012-ENS1_hec.nc"]

# use in_dir to grab all the filepaths with a .nc extension into a list of strings
in_dir = r"V:\projects\p00542_cpra_2020_lwi_t11\02_analysis\New_TSG_Analyses\Step4_ApplyBiasCor2\outputNCs_wTime_Python"
f = glob.glob(in_dir+"//*.nc") 

variables = ['rain']

# clip_shp = r"C:\jy\vortexImport\Truckee_River_Watershed_5mi_buffer\Truckee_River_Watershed_5mi_buffer.shp"

geo_options = {
    # 'pathToShp': clip_shp,
    # 'targetCellSize': '2000',
    # 'targetWkt': WktFactory.shg(),
    # 'resamplingMethod': 'Bilinear'
}

for afile in f:
    in_files = [afile]
    stormId = afile.split("-")[2]
    ensembleId = afile.split("-")[3]
    destination = afile.split(".")[0]+".dss"  
    # destination = r'C:\jy\vortexImport\JythonImport.dss'
    write_options = {
    'partA': stormId,
    'partF': ensembleId
    }

    # myImport = BatchImporter.builder() \
    #     .inFiles(in_files) \
    #     .variables(variables) \
    #     .geoOptions(geo_options) \
    #     .destination(destination) \
    #     .writeOptions(write_options) \
    #     .build()

    myImport = BatchImporter.builder() \
        .inFiles(in_files) \
        .variables(variables) \
        .destination(destination) \
        .writeOptions(write_options) \
        .build()

    myImport.process()
