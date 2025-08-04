import pandas as pd
from core.models import User, Order

df = pd.read_csv('orders.csv')

for _, row in df.iterrows():
    user_obj, _ = User.objects.get_or_create(
        user_id=row['user_id'],
        defaults={'gender': row['gender']}
    )

    Order.objects.create(
        order_id=row['order_id'],
        user=user_obj,
        status=row['status'],
        created_at=row['created_at'],
        returned_at=row['returned_at'] if pd.notna(row['returned_at']) else None,
        shipped_at=row['shipped_at'] if pd.notna(row['shipped_at']) else None,
        delivered_at=row['delivered_at'] if pd.notna(row['delivered_at']) else None,
        num_of_item=row['num_of_item']
    )
