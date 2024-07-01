from aiogram.types import ShippingOption , LabeledPrice

FAST_SHIPPING = ShippingOption(id="post_fast",
                               title="Tezkor yetkazib berish (1 ish kuni)",
                               prices=[LabeledPrice(label="Yetkazib berish xizmati", amount=4500000),
                                       LabeledPrice(label="Maxsus quti", amount=500000)])
REGULAR_SHIPPING = ShippingOption(id="post_regular",
                               title="Odatiy yetkazib berish (3 ish kuni)",
                               prices=[LabeledPrice(label="Yetkazib berish xizmati", amount=3500000),
                                       LabeledPrice(label="Maxsus quti", amount=500000)])
PICKUP_SHIPPING = ShippingOption(id="post_pickup",
                               title="Do'kondan olib ketish",
                               prices=[LabeledPrice(label="pickup",
                                                    amount=-10000000)])# yuz ming so'm