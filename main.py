import geopandas
import pandas as pd
import geopandas as gpd
import folium

'''
The datas come from a BDL GUS.pl - year 2020. Shapes of counties borders come from geoportal
The county is identified as a number - called TERYT, which is 7 length and triple zero at the end
'''
data_gus_average_m2 = 'RYNE_3788_CTAB_20220918022725.csv'
pd.options.mode.chained_assignment = None

average_m2_gus = pd.read_csv(data_gus_average_m2, delimiter=';')
average_m2_gus = average_m2_gus.iloc[:, 0:3]
average_m2_gus.columns = ['TERYT', 'Name', 'Price']

mapa_pow = gpd.read_file('map_data/a02_granice_powiatow.shp')
mapa_pow = mapa_pow[['JPT_KOD_JE', 'geometry']]
# print(mapa_pow)

average_m2_gus['TERYT_pow'] = average_m2_gus.TERYT.apply(lambda x: '0'+str(x) if len(str(x)) < 7 else str(x))
average_m2_gus['TERYT_pow'] = average_m2_gus.TERYT_pow.apply(lambda s: s[:4])
average_m2_gus = average_m2_gus[average_m2_gus['TERYT'] != '0']
data_gus_pow = average_m2_gus[average_m2_gus.TERYT_pow.str[0:3] != '000']

mapa_pow.geometry = mapa_pow.geometry.simplify(0.005)
pow_geoPath = mapa_pow.to_json()
mapa = folium.Map([52, 19], zoom_start=6)

folium.Choropleth(geo_data=pow_geoPath,  # GeoJSON
                  data=data_gus_pow,
                  columns=['TERYT_pow', 'Price'],
                  key_on='feature.properties.JPT_KOD_JE',  # key to GeoJSON
                  fill_color='YlOrRd',
                  fill_opacity=0.7,
                  line_opacity=0.2,
                  legend_name="Average price of one property square meter").add_to(mapa)

locations = {'1465': (52.230803, 21.010975), '1217': (49.297223, 19.949728), '3263': (53.902871, 14.283404), '2264': (54.441026, 18.563475)} # warsaw, zakopane, swinoujscie, sopot

for k, v in locations.items():
    folium.Marker(location=list(v), popup=data_gus_pow.loc[data_gus_pow['TERYT_pow'] == k, ['Name', 'Price']].values[0]).add_to(mapa)

mapa.save(outfile = 'averagem2.html')

# print(mapa_pow.dtypes)
# print(mapa_pow.sample(10))
# print(average_m2_gus.head())