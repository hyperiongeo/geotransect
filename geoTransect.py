from dataContainers import transectContainer

## These will be read from a config file .... ##
transect_file = 'data/transect_shp'
seismic_dir = 'data/seismic/'
las_shape = 'data/wells/'
elevation_file = 'data/elevation_raster/NS_DEM_ascii.asc'
extents = [0,40000, 6000,0]

# Initial the main object
tc = transectContainer(transect_file, seismic_dir, elevation_file,
                       las_shape, extents)

# Make the plots
tc.plot()

