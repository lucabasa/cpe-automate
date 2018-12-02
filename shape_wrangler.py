__author__ = "lucabasa"
__version__ = "1.0.0"

"""
Methods to get an overview of the police data

Other kinds of aggregations are possible

"""

import geopandas as gp


def find_geoid(city, pol, id_col='GEO.id2'):
	"""
	- city: geopandas DataFrame with the columns 'geometry' and the id_col
	- pol: geopandas DataFrame with a column 'geometry' containing points for every police event
	
	returns a list with the GEO.id2 relative to each point
	"""
    geoids = []
    for point in pol.geometry:
        try:
            geoids.append(city[city.geometry.contains(point)][id_col].values[0])
        except IndexError:
            geoids.append(np.nan)
    return geoids


def find_geoarea(shape_data, acs_data, dist_col='DISTRICT', id_col='GEO.id2'):
	"""
	Intersects the polygons of shape_data and acs_data and returns a geopandas DataFrame
	"""
	inter_shape = []
	for index, crim in shape_data.iterrows():
		for index2, popu in acs_data.iterrows():
		    if crim['geometry'].intersects(popu['geometry']):
		        inter_shape.append({'geometry': crim['geometry'].intersection(popu['geometry']),
		                     'district': crim[dist_col],
		                     id_col : popu[id_col],
		                     'area':crim['geometry'].intersection(popu['geometry']).area})
		        
	inter_shape = gp.GeoDataFrame(inter_shape,columns=['geometry', 'district', id_col,'area'])
	return inter_shape

