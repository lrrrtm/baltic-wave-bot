import json

from utils.volna_api import VolnaCard

volna = VolnaCard(card_number=215050004534
)

# print(json.dumps(volna.all_card_info, indent=4, ensure_ascii=False))
data = volna.get_top_up_link(1500)
print(data)

print(volna.get_order_status(order_id=data['orderId']))

