from utils.volna_api import VolnaCard

volna = VolnaCard(card_number=215050004534
)

data = volna.get_top_up_link(amount_cent=10000)
print(data)