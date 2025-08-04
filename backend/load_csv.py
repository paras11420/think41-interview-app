import os, csv, django, datetime
from dateutil import parser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User, Order

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_users():
    path = os.path.join(BASE_DIR, 'users.csv')
    print(f"Loading users from {path}...")
    
    count = 0
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                User.objects.update_or_create(
                    id = int(row['id']),
                    defaults = {
                        'first_name'  : row['first_name'],
                        'last_name'   : row['last_name'],
                        'email'       : row['email'],
                        'age'         : int(row['age']),
                        'gender'      : row['gender'],
                        'state'       : row['state'],
                        'street'      : row['street_address'],
                        'postal_code' : row['postal_code'],
                        'city'        : row['city'],
                        'country'     : row['country'],
                        'latitude'    : float(row['latitude']) if row['latitude'] else 0,
                        'longitude'   : float(row['longitude']) if row['longitude'] else 0,
                        'traffic_src' : row['traffic_source'],
                        'created_at'  : parser.parse(row['created_at'])
                    }
                )
                count += 1
                if count % 1000 == 0:
                    print(f"Loaded {count} users...")
            except Exception as e:
                print(f"Error loading user {row.get('id', 'unknown')}: {e}")
                continue
                
    print(f'✅  {count} Users loaded')

def load_orders():
    path = os.path.join(BASE_DIR, 'orders.csv')
    print(f"Loading orders from {path}...")
    
    count = 0
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            try:
                user_obj = User.objects.get(id=int(row['user_id']))
                Order.objects.update_or_create(
                    order_id = int(row['order_id']),
                    defaults = {
                        'user'        : user_obj,
                        'status'      : row['status'],
                        'gender'      : row['gender'],
                        'created_at'  : parser.parse(row['created_at']),
                        'returned_at' : parser.parse(row['returned_at'])  if row['returned_at']  else None,
                        'shipped_at'  : parser.parse(row['shipped_at'])   if row['shipped_at']   else None,
                        'delivered_at': parser.parse(row['delivered_at']) if row['delivered_at'] else None,
                        'num_of_item' : int(row['num_of_item'])
                    }
                )
                count += 1
                if count % 1000 == 0:
                    print(f"Loaded {count} orders...")
            except User.DoesNotExist:
                print(f"User {row['user_id']} not found for order {row['order_id']}")
                continue
            except Exception as e:
                print(f"Error loading order {row.get('order_id', 'unknown')}: {e}")
                continue
                
    print(f'✅  {count} Orders loaded')

if __name__ == '__main__':
    print("🚀 Starting data loading...")
    print("Available CSV files:", [f for f in os.listdir('.') if f.endswith('.csv')])
    load_users()
    load_orders()
    print('🎉  All data imported successfully!')
