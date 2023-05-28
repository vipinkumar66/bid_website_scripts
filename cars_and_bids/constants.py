import os
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

cwd = os.path.abspath(os.getcwd())
folder_name = os.path.join(cwd, 'Output_folder',
                            datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))

headers = ['yard_number', 'yard_name', 'sale_date', 'day_of_week', 'sale_time', 'time_zone', 'item',
            'lot_number', 'vehicle_type', 'year', 'make', 'model_group', 'model_detail', 'body_style', 'color',
            'damage_description', 'secondary_damage', 'sale_title_state', 'sale_title_type', 'has_keys',
            'lot_cond_code', 'vin', 'odometer', 'odometer_brand', 'est_retail_value', 'repair_cost', 'engine',
            'drive', 'transmission', 'fuel_type', 'cylinders', 'runs_drives', 'sale_status',
            'high_bid_non_vix_sealed_vix',
            'special_note', 'location_city', 'location_state', 'location_zip5', 'location_zip4',
            'location_country', 'currency_code', 'image_thumbnail', 'create_date_time', 'grid_row',
            'make_an_offer_eligible', 'buy_it_now_price', 'image_url', 'trim', 'last_updated_time', 'rentals',
            'copart_select', 'source', 'Timestamp']