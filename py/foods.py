"""Food database (per 100 g, cooked / ready-to-eat unless noted) and recipe library.

Nutrition values are typical reference values (USDA-style) rounded for planning.
Weights are COOKED / ready-to-eat weights; the shopping list converts to raw/dry weights.
"""

DIET_RANK = {"vegan": 0, "vegetarian": 1, "pescatarian": 2, "omnivore": 3}
CAT_RANK = {"plant": 0, "dairy": 1, "egg": 1, "fish": 2, "meat": 3}
ALLERGENS = ["dairy", "egg", "gluten", "nuts", "peanut", "sesame", "fish", "shellfish", "soy"]


def _f(name, k, p, c, f, fib, cat, alg="", aisle="Pantry", buy=1.0, unit=None, uname=None, step=10):
    return dict(name=name, kcal=k, p=p, c=c, f=f, fib=fib, cat=cat,
                alg=frozenset(x for x in alg.split(",") if x), aisle=aisle, buy=buy,
                unit=unit, uname=uname, step=step)


MEAT, DAIRY, GRAIN, PRODUCE, PANTRY = "Meat & fish", "Dairy & eggs", "Grains & bread", "Fruit & veg", "Pantry"

FOODS = {
    # --- meat & fish
    "chicken_breast": _f("Chicken breast, grilled", 165, 31, 0, 3.6, 0, "meat", "", MEAT, 1.33),
    "chicken_thigh": _f("Chicken thigh, skinless", 209, 26, 0, 10.9, 0, "meat", "", MEAT, 1.33),
    "lean_beef": _f("Lean beef / kofta mince, cooked", 185, 27, 0, 8, 0, "meat", "", MEAT, 1.35),
    "salmon": _f("Salmon, baked", 206, 22, 0, 12, 0, "fish", "fish", MEAT, 1.2),
    "hammour": _f("Hammour (grouper), grilled", 118, 25, 0, 1.3, 0, "fish", "fish", MEAT, 1.25),
    "tuna": _f("Tuna, canned in water", 116, 25.5, 0, 0.8, 0, "fish", "fish", MEAT, 1.0),
    "shrimp": _f("Shrimp, cooked", 99, 24, 0.2, 0.3, 0, "fish", "shellfish", MEAT, 1.2),
    # --- dairy & eggs
    "egg": _f("Whole eggs", 143, 12.6, 0.7, 9.5, 0, "egg", "egg", DAIRY, 1.0, 50, "egg", 50),
    "egg_white": _f("Egg whites", 52, 10.9, 0.7, 0.2, 0, "egg", "egg", DAIRY, 1.0, 33, "egg white", 33),
    "greek_yogurt": _f("Greek yogurt, low-fat", 59, 10, 3.6, 0.7, 0, "dairy", "dairy", DAIRY),
    "labneh": _f("Labneh, light", 110, 8, 5, 6.5, 0, "dairy", "dairy", DAIRY),
    "cottage": _f("Cottage cheese, low-fat", 72, 12, 2.7, 1, 0, "dairy", "dairy", DAIRY),
    "laban": _f("Laban / ayran, low-fat", 40, 3.3, 4.7, 1, 0, "dairy", "dairy", DAIRY),
    "milk": _f("Low-fat milk", 42, 3.4, 5, 1, 0, "dairy", "dairy", DAIRY),
    "feta": _f("Feta cheese", 264, 14, 4, 21, 0, "dairy", "dairy", DAIRY, 1.0, step=5),
    "whey": _f("Whey protein powder", 400, 80, 8, 6, 0, "dairy", "dairy", PANTRY, 1.0, 30, "scoop", 15),
    # --- plant protein
    "pea_protein": _f("Plant protein powder (pea)", 380, 80, 5, 6, 2, "plant", "", PANTRY, 1.0, 30, "scoop", 15),
    "tofu": _f("Firm tofu", 144, 17, 2.8, 8.7, 0.3, "plant", "soy", PRODUCE),
    "lentils": _f("Lentils, cooked", 116, 9, 20, 0.4, 7.9, "plant", "", PANTRY, 0.4),
    "chickpeas": _f("Chickpeas, canned & drained", 164, 8.9, 27.4, 2.6, 7.6, "plant", "", PANTRY),
    "foul": _f("Foul medames (fava beans), cooked", 110, 7.6, 19.6, 0.4, 5.4, "plant", "", PANTRY),
    # --- carbs
    "rice": _f("Basmati rice, cooked", 130, 2.7, 28, 0.3, 0.4, "plant", "", GRAIN, 0.35),
    "quinoa": _f("Quinoa, cooked", 120, 4.4, 21.3, 1.9, 2.8, "plant", "", GRAIN, 0.35),
    "oats": _f("Rolled oats (dry)", 389, 16.9, 66.3, 6.9, 10.6, "plant", "gluten", GRAIN, 1.0, step=5),
    "pita": _f("Whole-wheat khubz / pita", 260, 9.8, 53, 2.5, 7, "plant", "gluten", GRAIN, 1.0, 60, "pita", 15),
    "potato": _f("Potato, boiled", 87, 1.9, 20, 0.1, 1.8, "plant", "", PRODUCE),
    "sweet_potato": _f("Sweet potato, baked", 90, 2, 20.7, 0.2, 3.3, "plant", "", PRODUCE),
    # --- fruit & veg
    "banana": _f("Banana", 89, 1.1, 22.8, 0.3, 2.6, "plant", "", PRODUCE, 1.0, 120, "medium banana", 60),
    "apple": _f("Apple", 52, 0.3, 13.8, 0.2, 2.4, "plant", "", PRODUCE, 1.0, 180, "apple", 90),
    "berries": _f("Mixed berries", 50, 0.7, 12, 0.3, 3, "plant", "", PRODUCE),
    "dates": _f("Dates", 277, 1.8, 75, 0.2, 6.7, "plant", "", PRODUCE, 1.0, 24, "date", 24),
    "salad": _f("Mixed salad (cucumber, tomato, leaves)", 20, 1.2, 3.6, 0.2, 1.5, "plant", "", PRODUCE),
    "cucumber": _f("Cucumber", 15, 0.7, 3.6, 0.1, 0.5, "plant", "", PRODUCE),
    "tomato": _f("Tomato", 18, 0.9, 3.9, 0.2, 1.2, "plant", "", PRODUCE),
    "roasted_veg": _f("Roasted vegetables (zucchini, pepper, aubergine)", 45, 1.5, 8, 1.2, 2.5, "plant", "", PRODUCE),
    "broccoli": _f("Steamed broccoli", 35, 2.4, 7.2, 0.4, 3.3, "plant", "", PRODUCE),
    "tomato_stew": _f("Tomato & pepper sauce (shakshuka base)", 40, 1.6, 8, 0.6, 2, "plant", "", PRODUCE),
    # --- fats, nuts, spreads
    "olive_oil": _f("Olive oil", 884, 0, 0, 100, 0, "plant", "", PANTRY, 1.0, 5, "tsp", 5),
    "avocado": _f("Avocado", 160, 2, 8.5, 14.7, 6.7, "plant", "", PRODUCE),
    "almonds": _f("Almonds", 579, 21, 22, 50, 12.5, "plant", "nuts", PANTRY, 1.0, step=5),
    "walnuts": _f("Walnuts", 654, 15, 14, 65, 6.7, "plant", "nuts", PANTRY, 1.0, step=5),
    "peanut_butter": _f("Peanut butter", 588, 25, 20, 50, 6, "plant", "peanut", PANTRY, 1.0, step=5),
    "tahini": _f("Tahini", 595, 17, 21, 54, 9, "plant", "sesame", PANTRY, 1.0, step=5),
    "hummus": _f("Hummus", 166, 7.9, 14.3, 9.6, 6, "plant", "sesame", PRODUCE),
    "chia": _f("Chia seeds", 486, 17, 42, 31, 34, "plant", "", PANTRY, 1.0, step=5),
}

AISLE_ORDER = [MEAT, DAIRY, GRAIN, PRODUCE, PANTRY]


def _r(rid, name, cat, items, note=""):
    macros = dict(kcal=0.0, p=0.0, c=0.0, f=0.0, fib=0.0)
    rank, alg = 0, set()
    for key, g in items:
        fd = FOODS[key]
        macros["kcal"] += fd["kcal"] * g / 100
        macros["p"] += fd["p"] * g / 100
        macros["c"] += fd["c"] * g / 100
        macros["f"] += fd["f"] * g / 100
        macros["fib"] += fd["fib"] * g / 100
        rank = max(rank, CAT_RANK[fd["cat"]])
        alg |= fd["alg"]
    text = (name + " " + " ".join(FOODS[k]["name"] for k, _ in items)).lower()
    return dict(id=rid, name=name, cat=cat, items=items, note=note, m=macros, rank=rank,
                alg=frozenset(alg), text=text)


RECIPES = [
    # ---------------- breakfasts
    _r("shakshuka", "Shakshuka with whole-wheat khubz", "breakfast",
       [("egg", 150), ("tomato_stew", 200), ("pita", 60), ("olive_oil", 5)],
       "Simmer the sauce, crack in the eggs, cover until set."),
    _r("oats_yogurt", "Overnight oats with Greek yogurt & berries", "breakfast",
       [("oats", 50), ("greek_yogurt", 200), ("berries", 100), ("chia", 10)],
       "Mix the night before and keep chilled."),
    _r("foul_bowl", "Foul medames bowl", "breakfast",
       [("foul", 250), ("tomato", 100), ("olive_oil", 8), ("pita", 45)],
       "Warm the foul, top with chopped tomato and olive oil."),
    _r("white_omelette", "Egg-white omelette with veg & avocado", "breakfast",
       [("egg_white", 198), ("egg", 50), ("roasted_veg", 120), ("avocado", 40), ("pita", 45)],
       "Cook the omelette over medium heat, fill with vegetables."),
    _r("labneh_wrap", "Labneh, egg & salad wrap", "breakfast",
       [("pita", 60), ("labneh", 100), ("salad", 120), ("egg", 100), ("olive_oil", 3)],
       "Spread labneh, add sliced boiled eggs and salad, roll."),
    _r("protein_oats", "Protein oats with banana", "breakfast",
       [("oats", 60), ("whey", 30), ("banana", 120), ("peanut_butter", 10)],
       "Cook oats with water, stir in whey after cooking."),
    _r("cottage_fruit", "Cottage cheese, apple & walnuts", "breakfast",
       [("cottage", 200), ("apple", 180), ("walnuts", 15), ("chia", 5)],
       "Layer in a bowl."),
    _r("tuna_egg_toast", "Tuna & egg khubz with salad", "breakfast",
       [("tuna", 100), ("egg", 100), ("pita", 60), ("salad", 100)],
       "Mash tuna with a little lemon, serve on toasted khubz with boiled egg."),
    _r("tofu_scramble", "Tofu scramble with veg", "breakfast",
       [("tofu", 200), ("roasted_veg", 120), ("pita", 60), ("olive_oil", 5)],
       "Crumble tofu into a hot pan with the vegetables and spices."),
    _r("yogurt_chia_bowl", "Greek yogurt, berries & chia bowl", "breakfast",
       [("greek_yogurt", 250), ("berries", 120), ("chia", 15), ("dates", 24)],
       "Stir chia into the yogurt, top with berries and chopped dates."),
    _r("veg_egg_skillet", "Egg & vegetable skillet with avocado", "breakfast",
       [("egg", 150), ("roasted_veg", 200), ("avocado", 50), ("potato", 100)],
       "Fry the vegetables and potato, add the eggs and cover until set."),
    _r("foul_potato", "Foul medames with tomato & potato", "breakfast",
       [("foul", 250), ("tomato", 100), ("potato", 150), ("olive_oil", 8)],
       "Warm the foul, serve with chopped tomato and diced potato."),
    _r("tofu_sweet_potato", "Tofu scramble with sweet potato", "breakfast",
       [("tofu", 200), ("roasted_veg", 150), ("sweet_potato", 120), ("olive_oil", 3)],
       "Crumble tofu into a hot pan with spices, serve with baked sweet potato."),
    # ---------------- lunches & dinners
    _r("shawarma_bowl", "Chicken shawarma bowl (no bread)", "main",
       [("chicken_breast", 150), ("rice", 150), ("salad", 150), ("greek_yogurt", 40), ("olive_oil", 5)],
       "Spice-rub and grill the chicken; serve over rice with yogurt sauce."),
    _r("hammour_rice", "Grilled hammour with rice & roasted veg", "main",
       [("hammour", 180), ("rice", 150), ("roasted_veg", 150), ("olive_oil", 8)],
       "Grill with lemon and cumin."),
    _r("kofta_plate", "Lean kofta plate with hummus & salad", "main",
       [("lean_beef", 150), ("hummus", 50), ("salad", 200), ("pita", 45)],
       "Shape kofta with parsley and onion, grill."),
    _r("salmon_sweet_potato", "Salmon with sweet potato & broccoli", "main",
       [("salmon", 150), ("sweet_potato", 200), ("broccoli", 150), ("olive_oil", 5)],
       "Bake salmon and sweet potato together at 200°C for ~18 min."),
    _r("chicken_lentil_pot", "Chicken & lentil pot with roasted veg", "main",
       [("chicken_thigh", 120), ("lentils", 200), ("roasted_veg", 150), ("olive_oil", 5)],
       "Simmer lentils with cumin; serve with the chicken and vegetables."),
    _r("chickpea_curry", "Chickpea & veg curry with rice", "main",
       [("chickpeas", 200), ("roasted_veg", 200), ("rice", 120), ("greek_yogurt", 50), ("olive_oil", 5)],
       "Simmer chickpeas and vegetables in curry spices; finish with yogurt."),
    _r("tuna_quinoa", "Tuna quinoa salad with feta", "main",
       [("tuna", 130), ("quinoa", 150), ("salad", 200), ("olive_oil", 8), ("feta", 20)],
       "Toss everything with lemon juice."),
    _r("shrimp_stir_fry", "Shrimp & broccoli stir-fry with rice", "main",
       [("shrimp", 180), ("rice", 150), ("broccoli", 150), ("olive_oil", 8)],
       "Stir-fry on high heat with garlic and ginger."),
    _r("tofu_stir_fry", "Tofu & broccoli stir-fry with rice", "main",
       [("tofu", 200), ("rice", 150), ("broccoli", 150), ("tahini", 10)],
       "Pan-fry tofu until golden, toss with vegetables and tahini."),
    _r("chicken_avocado_salad", "Chicken & avocado salad with khubz", "main",
       [("chicken_breast", 150), ("salad", 250), ("avocado", 60), ("olive_oil", 5), ("pita", 40)],
       "Slice the chicken over the salad, dress with lemon and olive oil."),
    _r("lentil_soup_meal", "Lentil soup (shorbat adas) with salad", "main",
       [("lentils", 250), ("salad", 200), ("olive_oil", 8), ("pita", 60)],
       "Blend half of the soup for a creamy texture."),
    _r("beef_potato_tray", "Beef & potato tray bake", "main",
       [("lean_beef", 150), ("potato", 250), ("roasted_veg", 150), ("olive_oil", 5)],
       "Roast everything on one tray at 200°C."),
    _r("lentil_rice_bowl", "Lentil & rice bowl with roasted veg", "main",
       [("lentils", 250), ("rice", 120), ("roasted_veg", 200), ("olive_oil", 8)],
       "Season the lentils with cumin and garlic, serve over rice."),
    _r("chickpea_potato_tray", "Chickpea, potato & veg tray bake", "main",
       [("chickpeas", 200), ("potato", 200), ("roasted_veg", 200), ("olive_oil", 8)],
       "Roast everything with paprika and cumin at 200°C."),
    # ---------------- snacks
    _r("yogurt_berries", "Greek yogurt & berries", "snack",
       [("greek_yogurt", 200), ("berries", 100)], ""),
    _r("apple_almonds", "Apple & almonds", "snack",
       [("apple", 180), ("almonds", 20)], ""),
    _r("dates_laban", "Dates & laban", "snack",
       [("dates", 48), ("laban", 250)], ""),
    _r("whey_banana", "Protein shake with banana", "snack",
       [("whey", 30), ("milk", 250), ("banana", 120)], "Blend with ice."),
    _r("hummus_veg", "Hummus with cucumber & khubz", "snack",
       [("hummus", 60), ("cucumber", 150), ("pita", 30)], ""),
    _r("eggs_tomato", "Boiled eggs & tomato", "snack",
       [("egg", 100), ("tomato", 150)], ""),
    _r("cottage_cucumber", "Cottage cheese & cucumber", "snack",
       [("cottage", 150), ("cucumber", 100), ("olive_oil", 3)], ""),
    _r("tuna_cucumber", "Tuna cucumber boats", "snack",
       [("tuna", 80), ("cucumber", 120), ("olive_oil", 3)], ""),
    _r("pb_banana", "Banana with peanut butter", "snack",
       [("peanut_butter", 15), ("banana", 120)], ""),
    _r("nuts_dates", "Almonds & dates", "snack",
       [("almonds", 20), ("dates", 24)], ""),
    _r("tofu_cucumber", "Marinated tofu cubes & cucumber", "snack",
       [("tofu", 120), ("cucumber", 100)], ""),
    _r("pea_shake", "Plant protein shake with banana", "snack",
       [("pea_protein", 30), ("banana", 120)], "Blend with cold water and ice."),
    _r("whey_shake", "Whey protein shake (water)", "snack",
       [("whey", 30)], "Shake with cold water."),
    _r("egg_white_cup", "Egg-white scramble cup", "snack",
       [("egg_white", 198), ("tomato", 80)], ""),
]

BY_ID = {r["id"]: r for r in RECIPES}

# (slot key, label, share of daily kcal, recipe category)
LAYOUTS = {
    3: [("breakfast", "Breakfast", 0.28, "breakfast"), ("lunch", "Lunch", 0.38, "main"),
        ("dinner", "Dinner", 0.34, "main")],
    4: [("breakfast", "Breakfast", 0.25, "breakfast"), ("lunch", "Lunch", 0.33, "main"),
        ("snack1", "Afternoon snack", 0.12, "snack"), ("dinner", "Dinner", 0.30, "main")],
    5: [("breakfast", "Breakfast", 0.22, "breakfast"), ("snack1", "Mid-morning snack", 0.10, "snack"),
        ("lunch", "Lunch", 0.28, "main"), ("snack2", "Afternoon snack", 0.10, "snack"),
        ("dinner", "Dinner", 0.30, "main")],
}


def fmt_item(key, grams):
    fd = FOODS[key]
    qty = ""
    if fd["unit"]:
        n = grams / fd["unit"]
        nr = round(n * 2) / 2
        if abs(n - nr) < 0.05 and nr > 0:
            u = fd["uname"]
            if nr != 1 and not u.endswith(("s", "sp")):
                u += "s"
            qty = f"{nr:g} {u}"
    return {"key": key, "name": fd["name"], "grams": int(grams), "qty": qty}
