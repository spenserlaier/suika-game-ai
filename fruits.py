import collections
BASE_RADIUS = float(20)

lv_1_cherry = BASE_RADIUS
lv_2_strawberry = BASE_RADIUS*2
lv_3_grapes = BASE_RADIUS*2.5
lv_4_dekopon = BASE_RADIUS*3
lv_5_persimmon = BASE_RADIUS*3.5
lv_6_apple = BASE_RADIUS*4
lv_7_pear = BASE_RADIUS*5
lv_8_peach= BASE_RADIUS*5.5
lv_9_pineapple = BASE_RADIUS*6
lv_10_melon = BASE_RADIUS*7
lv_11_watermelon = BASE_RADIUS*8

next_sizes = collections.defaultdict(lambda: None)
next_sizes[lv_1_cherry] = lv_1_cherry*1.5
next_sizes[lv_2_strawberry] = lv_2_strawberry*1.5
next_sizes[lv_3_grapes] = lv_3_grapes*1.5
next_sizes[lv_4_dekopon] = lv_4_dekopon*1.5
next_sizes[lv_5_persimmon] = lv_5_persimmon*1.5
next_sizes[lv_6_apple] =  lv_6_apple*1.5
next_sizes[lv_7_pear] =  lv_7_pear*1.5
next_sizes[lv_8_peach] =  lv_8_peach*1.5
next_sizes[lv_9_pineapple] =  lv_9_pineapple*1.5
next_sizes[lv_10_melon] = lv_10_melon*1.5
next_sizes[lv_11_watermelon] = None #TODO: how to handle next_sizes for watermelon?


