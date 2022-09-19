import pandas as pd
import geopandas as gpd
import folium

data_gus_average_m2 = 'RYNE_3788_CTAB_20220918022725.csv'

average_m2_gus = pd.read_csv(data_gus_average_m2, delimiter=';')
average_m2_gus = average_m2_gus.iloc[:, 0:3]
average_m2_gus.columns = ['TERYT', 'Name', 'Price']

mapa_pow = gpd.read_file('map_data/a02_granice_powiatow.shp')
mapa_pow = mapa_pow[['JPT_KOD_JE', 'geometry']]
print(mapa_pow)
average_m2_gus['TERYT_pow'] = average_m2_gus.TERYT.apply(lambda x: '0'+str(x) if len(str(x)) < 7 else str(x)) # TERYT should be 7 length
average_m2_gus['TERYT_pow'] = average_m2_gus.TERYT_pow.apply(lambda s: s[:4])
average_m2_gus = average_m2_gus[average_m2_gus['TERYT'] != '0']
data_gus_pow = average_m2_gus[average_m2_gus.TERYT_pow.str[0:3] != '000']
print(data_gus_pow)
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

mapa.save(outfile = 'averagem2.html')


# print(mapa_pow.dtypes)
# print(mapa_pow.sample(10))
# print(average_m2_gus.head())
# print(data_gus_pow.sample(20))