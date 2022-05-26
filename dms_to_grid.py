from osgeo import osr
from math import ceil
from pyproj import CRS


def get_utm_zone(lon):
    return int(1 + (lon + 180.0) / 6.0)


def is_utm_northern(lat):
    if lat < 0.0:
        return True
    else:
        return False


def get_utm_crs(lon, lat):
    zone = get_utm_zone(lon)
    south = not is_utm_northern(lat)
    crs = CRS.from_dict({'proj': 'utm', 'zone': zone, 'south': south})
    print(crs.to_authority())
    return int(crs.to_authority()[1])  # returns EPSG code only


if __name__ == "__main__":
    # EXAMPLE coordinates (not real):
    radar_lat = 57.98
    radar_lon = 33.25
    meteo_lat = 57.66
    meteo_lon = 32.52
    # resolution of radar image:
    res = 2000  # meters
    # size of radar grid, cells:
    size = 252
    radar_grid_x = size / 2
    radar_grid_y = size / 2

    s_srs = osr.SpatialReference()
    s_srs.ImportFromEPSG(4326)
    # print("Source SRS is: %s" % s_srs)
    t_srs = osr.SpatialReference()
    t_srs_epsg_code = get_utm_crs(radar_lon, radar_lat)
    # print(t_srs_epsg_code)
    t_srs.ImportFromEPSG(t_srs_epsg_code)
    # print("Target SRS is: %s" % t_srs)
    ct = osr.CoordinateTransformation(s_srs, t_srs)
    # print(ct)
    radar_e, radar_n, radar_h = ct.TransformPoint(radar_lat, radar_lon)
    # print(radar_e, radar_n)
    meteo_e, meteo_n, meteo_h = ct.TransformPoint(meteo_lat, meteo_lon)
    # print(meteo_e, meteo_n)
    de = meteo_e - radar_e
    dn = meteo_n - radar_n
    print(de, dn)
    grid_de = de / res
    grid_dn = dn / res
    print(grid_de, grid_dn)

    meteo_grid_x = ceil(radar_grid_x + grid_de)
    meteo_grid_y = ceil(radar_grid_y + grid_dn)
    print(meteo_grid_x, meteo_grid_y)
