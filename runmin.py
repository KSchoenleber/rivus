import capmin
import pandashp as pdshp
import pandaspyomo as pdpo
from coopr.opt.base import SolverFactory

building_shapefile = 'data/mnl/mnl_building'
edge_shapefile = 'data/mnl/mnl_edge'
vertex_shapefile = 'data/mnl/mnl_vertex'
data_spreadsheet = 'data/mnl/mnl.xlsx'


# load buildings and sum by type and nearest edge ID
# 1. read shapefile to DataFrame (with special geometry column)
# 2. group DataFrame by columns 'nearest' (ID of nearest edge) and 'type'
#    (residential, commercial, industrial, other)
# 3. sum by group and unstack, i.e. convert secondary index 'type' to columns
buildings = pdshp.read_shp(building_shapefile)
buildings_grouped = buildings.groupby(['nearest', 'type'])
total_area = buildings_grouped.sum()['total_area'].unstack()

# load edges (streets) and join with summed areas 
# 1. read shapefile to DataFrame (with geometry column)
# 2. join DataFrame total_area on index (=ID)
# 3. fill missing values with 0
edges = pdshp.read_shp(edge_shapefile)
edges_w_area = edges.join(total_area)
edges_w_area = edges_w_area.fillna(0)

# load nodes
nodes = pdshp.read_shp(vertex_shapefile)

# create model
model = capmin.create_model(data_spreadsheet, nodes, edges_w_area)
instance = model.create()
solver = SolverFactory('glpk')

# solve problem
#result = solver.solve(instance)
#instance.load(result)

instance.write()
