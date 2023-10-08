import pandas as pd
import numpy as np

df = pd.read_json("/Users/pc/Documents/GitHub/myauto-scraping-tool/data.jl", lines= True)

new_df_inner_api_call = pd.json_normalize(df['inner_api_call'])
new_df_statemet_card = pd.json_normalize(df['statemet_card'])

new_df_inner_api_call.columns = new_df_inner_api_call.columns.str.replace('info.', '')

final_df = new_df_inner_api_call[['car_id', 'prod_year', 'price_usd', 'car_run_km', 'customs_passed', 'model_id', 'location_id','parent_loc_id', 'tech_inspection', 'for_rent',
'predicted_price', 'auction_date', 'active_ads', 'end_date', 'views', 'has_predicted_price', 'pred_first_breakpoint', 'pred_second_breakpoint',
'pred_min_price','pred_max_price']].copy()

final_df.loc[:, 'vin_number'] = new_df_statemet_card.loc[:, 'vin']

final_df['vin_number'] = final_df['vin_number'].replace('', np.nan)

location_variable = "2.3.4.7.15.30.113.52.37.36.38.39.40.31.5.41.44.47.48.53.54.8.16.6.14.13.12.11.10.9.55.56.57.59.58.61.62.63.64.66.71.72.74.75.76.77.78.80.81.82.83.84.85.86.87.88.91.96.97.101.109"
list_of_locations = location_variable.split('.')
list_of_locations = [eval(i) for i in list_of_locations]

print(list_of_locations)

final_df = final_df[(final_df.prod_year >= 2020)]
final_df = final_df[final_df.vin_number.notnull()]
final_df = final_df[(final_df.car_run_km <= 50000)]
final_df = final_df[(final_df.views <= 200)]
final_df = final_df[final_df['location_id'].isin(list_of_locations)]
final_df = final_df[(final_df.customs_passed == 0)]

vin_csv = final_df[['car_id', 'vin_number', 'location_id']]
vin_csv.describe()

vin_csv.to_csv('vin_records.csv')