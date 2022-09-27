# This script is meant to match the functionality of nc2RAS.m Matlab script
# Converts an input netCDF file to be used  for the 500 different equiprobable rainfall fields derived from the IPET predicted rainfall for selected historic rainfall events
# Myles McManus, TWI 2022

# Import List of selected historic rainfall events and their respective startTimes
import glob, os
import pandas as pd
from datetime import datetime
import xarray as xr

stormListFileName = "LWI_Phase2Storms_EBTRK_Times.csv"
stormList = pd.read_csv(stormListFileName)
stormList

#Check folder for input files
os.chdir("./input")
filenameList = []
for file in glob.glob("*.nc"):
    filenameList.append(file)
filenameList
os.chdir("..")

for file in filenameList:
    outFilename = file.split(".")[0] + "-hec.nc"
    stormID = file.split(".")[0].split("-")[2]
    ensembleID = file.split(".")[0].split("-")[3]
    # Look up startTime from stormList by stormID
    try:
        startTime_str = stormList[stormList['StormID'].str.contains(stormID, na=False, case=False)]['StartTime'].values[0]
    except:
        print (f'{stormID} not found in {stormListFileName}')
    startTime_dt = datetime.strptime(startTime_str, '%m/%d/%y %H:%M')
    startTime_str_formatted = datetime.strftime(startTime_dt, '%Y-%m-%d %H:%M:00')
    
    # open input nc, edit to make HEC compliant, save as output nc
    ds = xr.open_dataset("./input/"+file)

    varNames = {'lon': 'x', 'lat': 'y', 'timestep': 'time', 'tcr': 'rain'}
    ds = ds.rename(varNames)

    ds.time.attrs['units'] = f'minutes since {startTime_str_formatted}'
    ds.time.attrs['standard_name'] = 'time'
    ds.time.attrs['long_name'] = 'time'
    ds.time.attrs['axis'] = 'T'

    ds.x.attrs['units'] = 'degrees_east'
    ds.y.attrs['units'] = 'degrees_north'
    ds.x.attrs['long_name'] = 'Longitude'
    ds.y.attrs['long_name'] = 'Latitude'
    ds.x.attrs['axis'] = 'X'
    ds.y.attrs['axis'] = 'Y'
    ds

    ds = ds.assign({
        'crs' : (
            (),
            0
        )
    })

    ds.crs.attrs = {
        'long_name': 'coordinate reference system',
        'epsg_code': 'EPSG:4326',
        'crs_wkt' : 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]',
        'semi_major_axis' : 6378137.0,
        'semi_minor_axis' : 6356752.314245179,
        'inverse_flattening' : 298.257223563,
        'reference_ellipsoid_name' : 'WGS 84',
        'longitude_of_prime_meridian' : 0.0,
        'prime_meridian_name' : 'Greenwich',
        'geographic_crs_name' : 'WGS 84',
        'grid_mapping_name' : 'latitude_longitude',
        'spatial_ref' : 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]',
    }
 
    ds.rain.attrs['long_name'] = 'Total rainfall accumulation over 20 minutes'
    ds.rain.attrs['units'] = 'mm'
    # ncwriteatt(ncfileout,'UD','grid_mapping','crs')
    ds.rain.attrs['grid_mapping'] = 'crs'
    ds.rain.attrs['_FillValue'] = -999

    ds.attrs = {
        'Conventions':'CF-1.6,UGRID-0.9',
        'title': f'{stormID}',
        'ensembleID': f'{ensembleID}',
        'institution': 'The Water Institute',
        'source': f'LWI Storm Generator {file}',
        'Metadata_Conventions': 'Unidata Dataset Discovery v1.0',
        'summary': 'LWI_Phase2_Synthetic_Rainfall. 500 different equiprobable rainfall fields derived from the IPET predicted rainfall for selected historic rainfall events',
        'date_created': f"{datetime.today().strftime('%Y-%m-%d')}",
        }

    ds.to_netcdf(path="./output/"+outFilename, format="NETCDF4", engine="netcdf4")
    print (f"\n{outFilename} Successfully Written to Disk.")