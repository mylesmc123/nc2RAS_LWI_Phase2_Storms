clear all
close all
fclose all


%%% USER INPUTS      format = 2012-08-20 12:00:00.0
startDateStrings={... 
    '2004-10-08 12:00:00.0';...
    '2005-09-18 00:00:00.0';...
    '2012-08-20 12:00:00.0'};

% units for rainfall 1=mm 2=inches
Runits = 2;

% ---- check folder for input files
inputDir = 'netCDFOut/*.nc';
fileinfo = dir(inputDir);
fnames = {fileinfo.name};
szfnames = length(fnames);

%define output folder
if not(isfolder('outputNCs_wTime'))
    mkdir('outputNCs_wTime');
end


%--- Loop through input files
for i = 1:szfnames
    
    %define output file
    fileID = erase(fnames{i},'.nc');
    tempStr = strsplit(fileID,'-');
    stormID = string(tempStr(3));
    if Runits == 1
        suffix = '_mm.nc';
    elseif Runits == 2
        suffix = '_in.nc';
    end
    ncfileout=['outputNCs_wTime/',fileID,suffix];%name of output file


%% ----- read in original netCDF data    
    file = ['netCDFOut/',fnames{i}];
    % ncdisp(file);


    %read in time, re-time in elapsed minutes (CHANGE as NECESSARY)
    timestep=ncread(file,'timestep'); 
    startTime = 0;
    elapsedTime = 0;
    for i =1:length(timestep)
        time(i) = startTime + elapsedTime;
        elapsedTime = elapsedTime + 20;
    end
    time = time';

    %read in lat and long
    lat=ncread(file,'lat');     
    lon=ncread(file,'lon');
    %read in parameter value matrix
    data=ncread(file,'tcr');
    if Runits == 2
        data = data .* 0.0393701; %in/mm
    end
    
    
    
 %% --- write in new NetCDF as per Max Agnew's template
    %create and write new netCDF file variable
    delete(ncfileout)
    nccreate(ncfileout,'rain','Dimensions',{'x',length(lon),'y',length(lat),'time',length(time)},'Format','classic','datatype','single')
    nccreate(ncfileout,'time','Dimensions',{'time',length(time)},'Format','classic')
    nccreate(ncfileout,'x','Dimensions',{'x',length(lon)},'Format','classic')
    nccreate(ncfileout,'y','Dimensions',{'y',length(lat)},'Format','classic')
    nccreate(ncfileout,'crs','Format','classic','datatype','int32')
    
    ncwrite(ncfileout,'rain',data)
    ncwrite(ncfileout,'time',time)
    ncwrite(ncfileout,'x',lon)
    ncwrite(ncfileout,'y',lat)

  %and whatever the heck this is (from Max Agnew's script)
  Ab= {'Conventions','CF-1.6,UGRID-0.9';
    'title','Data';
    'institution','MVN USACE';
    'source','Export NETCDF-CF_GRID from ADCIRC';
    'history','2018-04-20 13:30:52 GMT: exported from ADCIRC';
    'references','http://';
    'Metadata_Conventions','Unidata Dataset Discovery v1.0';
    'summary','Data exported from ADCIRC';
    'date_created','2020-12-20 13:30:52 GMT';
    'fews_implementation_version','2017.01';
    'fews_patch_number','73948';
    'fews_build_number','71514'};

    for f = 1:12
    ncwriteatt(ncfileout,'/',char(Ab(f,1)),char(Ab(f,2)));
    end

ncwriteatt(ncfileout,'time','standard_name','time')
ncwriteatt(ncfileout,'time','long_name','time')
% use the correct start time as defined by runID
if stormID == 'MATTHEW_2004'
    ii=1;
elseif stormID == 'RITA_2005'
    ii=2;
elseif stormID == 'ISAAC_2012'
    ii=3;
end

ncwriteatt(ncfileout,'time','units',['minutes since ',char(startDateStrings(ii)),' +0000']) 
ncwriteatt(ncfileout,'time','axis','T')

ncwriteatt(ncfileout,'y','standard_name','latitude')
ncwriteatt(ncfileout,'y','long_name','y coordinate according to WGS 1984')
ncwriteatt(ncfileout,'y','units','degrees_north')
ncwriteatt(ncfileout,'y','axis','Y')
ncwriteatt(ncfileout,'y','_FillValue',9.96921000000000e+36)

ncwriteatt(ncfileout,'x','standard_name','longitude')
ncwriteatt(ncfileout,'x','long_name','x coordinate according to WGS 1984')
ncwriteatt(ncfileout,'x','units','degrees_east')
ncwriteatt(ncfileout,'x','axis','X')
ncwriteatt(ncfileout,'x','_FillValue',9.96921000000000e+36)

ncwriteatt(ncfileout,'crs','long_name','coordinate reference system')
ncwriteatt(ncfileout,'crs','grid_mapping_name','latitude_longitude')
ncwriteatt(ncfileout,'crs','longitude_of_prime_meridian',0)
ncwriteatt(ncfileout,'crs','semi_major_axis',6378137)
ncwriteatt(ncfileout,'crs','inverse_flattening',298.257223563000)
ncwriteatt(ncfileout,'crs','crs_wkt','GEOGCS["WGS 84", DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]], PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]], UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]], AUTHORITY["EPSG","4326"]]')
ncwriteatt(ncfileout,'crs','proj4_params','+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
ncwriteatt(ncfileout,'crs','epsg_code','EPSG:4326')

ncwriteatt(ncfileout,'rain','long_name','rainfall')
if Runits == 1
    ncwriteatt(ncfileout,'rain','units','mm') 
elseif Runits == 2
   ncwriteatt(ncfileout,'rain','units','in') 
end
ncwriteatt(ncfileout,'rain','_FillValue',-999)
ncwriteatt(ncfileout,'rain','grid_mapping','crs')

end







