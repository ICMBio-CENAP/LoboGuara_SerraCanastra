# Land use map - maned wolf
# Refining land use map

python

# Import modules
import os
import grass.script as grass

# Land use map
land_use_map_input = 'Mapa_final_AreaLobo_raster'

# Region
grass.run_command('g.region', raster = land_use_map_input)

# Areas of cloud, queimada, and exposed soil
expression = 'clouds_etal = if('+land_use_map_input+' == 37 || '+land_use_map_input+' == 56 || '+land_use_map_input+' == 60, 1, null())'
grass.mapcalc(expression, overwrite = True)

# Areas of that are not cloud, queimada, and exposed soil
expression = 'non_clouds_etal = if('+land_use_map_input+' != 37 && '+land_use_map_input+' != 56 && '+land_use_map_input+' != 60, 1, null())'
grass.mapcalc(expression, overwrite = True)

# Land use in areas of that are not cloud, queimada, and exposed soil
expression = 'land_use_non_clouds_etal = if('+land_use_map_input+' != 37 && '+land_use_map_input+' != 56 && '+land_use_map_input+' != 60, '+land_use_map_input+', null())'
grass.mapcalc(expression, overwrite = True)

# Moving window of the land use map - 200m (81)
grass.run_command('r.neighbors', input = 'land_use_non_clouds_etal', output = 'mode_land_use_no_clouds_etal_200m',
                  size = 41, method = 'mode')

# Filling gaps with the moving window map above
grass.run_command('r.patch', input = 'land_use_non_clouds_etal,mode_land_use_no_clouds_etal_200m', output = 'land_use_filled_200m', overwrite = True)

# Identifying only empty gaps
expression = 'still_clouds_200m = if(isnull(land_use_filled_200m), 1, null())'
grass.mapcalc(expression, overwrite = True)

# Checking the maximum distance from a cloud (null) cell to a land use cell, to define the next moving window size
grass.run_command('r.grow.distance', input = 'land_use_filled_200m', distance = 'land_use_filled_200m_dist')

# Metadata (r.info): maximum distance = 410m
grass.run_command('r.info', map = 'land_use_filled_200m_dist')

# g.region only where there are clouds
grass.run_command('g.region', zoom = 'still_clouds_200m')
grass.run_command('g.region', raster = land_use_map_input)

# 2nd Moving window of the land use map - 835m (167)
grass.run_command('r.neighbors', input = 'land_use_filled_200m', selection = 'still_clouds_200m',
                  output = 'mode_land_use_no_clouds_etal_200m_835m',
                  size = 167, method = 'mode', overwrite = True)

# Reclassify varzea as campo
expression = 'land_use_no_clouds_etal_mode_200m_835m_varzea_as_campo = if(mode_land_use_no_clouds_etal_200m_835m == 35, 16, mode_land_use_no_clouds_etal_200m_835m)'
grass.mapcalc(expression, overwrite = True)

# Reclassify cafe as agricultura
expression = 'land_use_gaps_filled_varzea_as_campo_cafe_as_crops = if(land_use_no_clouds_etal_mode_200m_835m_varzea_as_campo == 33, 36, land_use_no_clouds_etal_mode_200m_835m_varzea_as_campo)'
grass.mapcalc(expression, overwrite = True)

# Reclassify mata pioneira inicial as mata inicial
expression = 'land_use_gaps_filled_varzea_as_campo_cafe_as_crops_pioneira_as_inicial = if(land_use_gaps_filled_varzea_as_campo_cafe_as_crops == 11, 12, land_use_gaps_filled_varzea_as_campo_cafe_as_crops)'
grass.mapcalc(expression, overwrite = True)

# Export output
grass.run_command('g.region', raster = land_use_map_input)

os.chdir(r'/home/leecb/Documentos/UNESP/analises/rogerio_lobos/data/land_use_map')

grass.run_command('r.out.gdal', input = 'land_use_gaps_filled_varzea_as_campo_cafe_as_crops_pioneira_as_inicial', 
                  output = 'land_use_gaps_filled_varzea_as_campo_cafe_as_crops_pioneira_as_inicial.tif', 
                  createopt = 'TFW=YES,COMPRESS=DEFLATE')





