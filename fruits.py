import collections
import random
import colors
BASE_RADIUS = float(20)

lv_1_cherry = BASE_RADIUS
lv_2_strawberry = BASE_RADIUS*2
lv_3_grapes = BASE_RADIUS*3
lv_4_dekopon = BASE_RADIUS*3.5
lv_5_persimmon = BASE_RADIUS*4
lv_6_apple = BASE_RADIUS*4.5
lv_7_pear = BASE_RADIUS*5.5
lv_8_peach= BASE_RADIUS*6
lv_9_pineapple = BASE_RADIUS*6.5
lv_10_melon = BASE_RADIUS*7
lv_11_watermelon = BASE_RADIUS*8

fruit_vals = [lv_1_cherry,
              lv_2_strawberry,
              lv_3_grapes,
              lv_4_dekopon,
              lv_5_persimmon,
              lv_6_apple,
              lv_7_pear,
              lv_8_peach,
              lv_9_pineapple,
              lv_10_melon,
              lv_11_watermelon
              ]

scores = dict()
scores[lv_1_cherry] = 1
scores[lv_2_strawberry] = 3
scores[lv_3_grapes] = 6
scores[lv_4_dekopon] = 10
scores[lv_5_persimmon] = 15
scores[lv_6_apple] = 21
scores[lv_7_pear] = 28
scores[lv_8_peach] = 36
scores[lv_9_pineapple] = 45
scores[lv_10_melon] = 55
scores[lv_11_watermelon] = 66

available_colors = set()
while len(available_colors) < 11:
    available_colors.add(colors.generate_color())

fruit_colors = dict()
idx = 0
for c in available_colors:
    fruit_val = fruit_vals[idx]
    fruit_colors[fruit_val] = c
    idx += 1



next_sizes = collections.defaultdict(lambda: None)
# TODO: refactor to use the array. arr[idx] = arr[idx + 1] for all except last
next_sizes[lv_1_cherry] = lv_2_strawberry
next_sizes[lv_2_strawberry] = lv_3_grapes
next_sizes[lv_3_grapes] = lv_4_dekopon
next_sizes[lv_4_dekopon] = lv_5_persimmon
next_sizes[lv_5_persimmon] = lv_6_apple
next_sizes[lv_6_apple] =  lv_7_pear
next_sizes[lv_7_pear] =  lv_8_peach
next_sizes[lv_8_peach] =  lv_9_pineapple
next_sizes[lv_9_pineapple] =  lv_10_melon
next_sizes[lv_10_melon] = lv_11_watermelon
next_sizes[lv_11_watermelon] = None #TODO: how to handle next_sizes for watermelon?


