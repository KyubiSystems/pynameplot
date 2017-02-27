# Generate list of coordinates for gridsquare
# input 4-tuple of grid TLC, dlongitude, dlatitude
# return list of 4 coords for grid corners

def gridsquare(coords):
    (lon, lat, dlon, dlat) = coords
    gs = [(lon, lat), (lon - dlon, lat), (lon-dlon, lat-dlat), (lon, lat-dlat)]
    return gs
