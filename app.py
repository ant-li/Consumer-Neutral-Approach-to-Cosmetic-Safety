import numpy as np
import pandas as pd
import streamlit as st
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report
from collections import Counter
# import time

dry = ['hyaluronic acid', 'glycerin', 'aloe vera', 'shea butter',
       'simmondsia chinensis (jojoba) leaf extract', 'niacinamide']
# def count_down(ts):
#         while ts:
#             mins, secs = divmod(ts, 60)
#             time_now = '{:02d}:{:02d}'.format(mins, secs)
#             print(f"{time_now}")
#             time.sleep(1)
#             ts -= 1

st.markdown('''
# **Consumer-Neutral Approach to Cosmetic Safety**
''')
st.write('**Please Select Your Skin Type**')

# skincare ingredients database
ingredients = pd.read_csv('skincare_ingredients - Sheet1.csv')
ingredients['is_vegan_friendly'] = ingredients['is_vegan_friendly'].str.strip(
    ' ')
ingredients.at[0, 'animal_based'] = 'yes'
ingredients['other_names'] = ingredients['other_names'].str.lower()


# skin_type is type str, will use for future analysis
skin_type = st.selectbox('If you\'re unsure, select a type to learn more about it!', [
                         'Select', 'Dry', 'Normal', 'Combination', 'Oily', 'Sensitive'])


if skin_type == 'Dry':
    st.write('Dry skin type lacks **moisture and natural oils**. If your skin is prone to **roughness, flakiness, or even itchiness**, you may have dry skin type. Another indication of dry skin include uncomfortable **tightness in the skin**.')
elif skin_type == 'Sensitive':
    st.write('Sensitive skin type **can be any of the other skin types** but can be prone to **burning-sensations, itchiness, or dryness**. This means that certain ingredients and products can cause unwanted reactions. If you react poorly to a lot of cosmetic products, your skin may also be sensitive.')
elif skin_type == 'Normal':
    st.write('Normal skin type is neither dry or oily and pertains to a well balanced skin type. That means you won\'t run into many issues like other skin types (but having a balanced skincare routine is still important). Lucky you :)!')
elif skin_type == 'Combination':
    st.write('Combination skin type comes with **both oily and dry parts around your skin**. The T-zone is typically known to be oily (the forhead, nose,and chin), while the cheek area is either dry or normal. If your skin feels oily in some parts while not in others, your might have combination skin type.')
elif skin_type == 'Oily':
    st.write('Oily skin type **produces excess oil and sebum** and can lead to a **greasy look**. If your skin is prone to **large pores/blackheads along with acne blemishes**, you may have oily skin type.')

# st.write(skincare_ingred)
# text seperater
st.write("___")

# write in the ingredients they are looking for

st.write('#### **Copy in The Product\'s Ingredients**')
curr_ingreds = st.text_input(
    'Enter your ingredients in comma-seperated format:')

# if t
curr_ingreds = curr_ingreds.lower().replace(' ', '').split(",")

found_count = 0
found = np.array([])
not_found = np.array([])

# breakdown on what ingredients were found and which were not
for ingredient in curr_ingreds:
    found_base = ingredient in ingredients['ingredient'].unique()
    found_alt = (ingredients['other_names'] == ingredient).fillna(False)
    
    if found_base:
        found = np.append(found, ingredient)
        found_count += 1
    elif any(found_alt):
        found = np.append(
            found, ingredients[found_alt]['ingredient'].iloc[0])
        found_count += 1
    else:
        not_found = np.append(not_found, ingredient)
#st.write(found)
if len(curr_ingreds) > 1:
    st.write(
        f' **{found_count} ingredients** were found to have significant information:')
    st.write(", ".join(found))
    st.write("___")
    st.write(
        f' **{len(curr_ingreds) - found_count} ingredients** were not found to have significant information:')
    st.write(", ".join(not_found))

st.write("___")

# what does our consumers care about?
st.write("#### What do you care about in your cosmetic products?")
options = st.multiselect(
    'Select all that apply and we\'ll tell you if your product is fit for you',
    ['Cruelty-Free/Vegan', 'Pretroleum-Free', 'Mineral-Free', 'Paraben-Free', 'Fragrance-Free', 'Natural Ingredients'])
st.write("____")

# ready = st.button('generate product analysis')

# loading_placeholder = st.empty()
# if ready:
#         loading_placeholder.write('**loading...**')
#         count_down(3)
#         loading_placeholder.empty()

st.write("#### What do you want to know about your product?")
col1, col2, col3, col4 = st.columns([2.3, 2.6, 2.5, 2.4])
with col1:
    butt_1 = st.empty().button('Ingredient Benefits')
with col2:
    butt_2 = st.empty().button('Ingredient Background')
with col3:
    butt_3 = st.empty().button('Ingredient Proposed Risks')
with col4:
    butt_4 = st.empty().button('Ingredient Functions')


loading_placeholder = st.empty()
info_placeholder = st.empty()

# get all of the found ingredients so we can use for further analysis
ingred_info_df = ingredients[ingredients['ingredient'].isin(found)]
# breakdown of ingredients by benefits
if butt_1:

    benefit_count = ingred_info_df['known_benefits'].dropna(
    ).str.split(', ').apply(Counter).reset_index(drop=True)
    list_of_dicts = list(benefit_count)
    merged_dict = {}

    for dict in list_of_dicts:
        for key, value in dict.items():
            if key in merged_dict:
                merged_dict[key] += value
            else:
                merged_dict[key] = value
    st.write('##### What Are The Ingredients\' Benefits?')
    for (key, value) in merged_dict.items():
        ingred_list = ingred_info_df[ingred_info_df['known_benefits'].fillna(
            'None').str.contains(key)]['ingredient']
        st.markdown(f'''There were **{str(value)} ingredient(s)** in this product that have benefits towards **{str(key)}**:    
        {', '.join(str(x) for x in list(ingred_list))}
        ''')
        st.write("____")

    # how does the ingredients compare to their skin type
    if skin_type == 'Select':
        st.write(
            '**select a skin type from the selection above to compare how this product may affect your skin**')
    else:
        st.write('##### How Does This Compare to Your Skin Type?')
        if skin_type == 'Normal':
            st.write('Normal have known issues, however, look at benefits that could help your skion')
        if skin_type == 'Dry':
            # For dry skin, look for ingredients that promote **hydration** and **nourishment**.
            st.markdown('''Here\'s how these ingredients may affect dry skin:            
            ''')

            contains_hydration = 'hydration' in merged_dict.keys()

            # hydration is key for dry skin
            if contains_hydration:
                lots_of_hydration = merged_dict['hydration'] > 2
                if lots_of_hydration:
                    st.write(
                        '1. This product contains ***three or more*** hydrating ingredients, beneficial to helping you reduce flaky and tight skin.')
                else:
                    st.write('1. This product contains ***less than three*** hydrating ingredients. If your skin tends to be on the more dryer side, more hydrating ingredients may be beneficial.')
            else:
                st.write('1. This product contains no hydrating ingredients, dry skin actively looks for products/ingredients that promote **hydration** and **nourishment** to the skin. Looking for products that have more hydrating ingredients may be beneficial.')

            # soothing helps lock in moisture
            contains_soothing = 'soothing' in merged_dict.keys()

            if contains_soothing:
                lots_of_soothing = merged_dict['soothing'] > 2
                if lots_of_soothing:
                    st.write('2. This product contains ***three or more*** soothing ingredients, beneficial to helping repair your skin barrier and inflammation that appear in dry skin.')
                else:
                    st.write('2. This product contains ***less than three*** soothing ingredients. If your skin tends to have inflammation and poor skin barrier, more soothing ingredients may be beneficial.')
            else:
                st.write('2. This product contains no soothing ingredients, dry skin actively looks for products/ingredients that promote a **healthy skin barrier**  to the skin. Looking for products that have more soothing ingredients may be beneficial.')
            # should go against oil control since dry skin lacks oil

            contains_oil = 'oil control' in merged_dict.keys()
            if contains_oil:
                lots_of_oil = merged_dict['oil control'] > 2
                if lots_of_oil:
                    st.write('3. This product contains ***three or more*** oil control ingredients. This can strip your natural oils more than you need to. Dry skin looks for more nourishing ingrdients rather than ingredients that help control oil.')

            contains_aging = 'anti-aging' in merged_dict.keys()

            if contains_aging:
                lots_of_aging = merged_dict['anti-aging'] > 2
                if lots_of_aging:
                    st.write('4. This product contains ***three or more*** anti-aging ingredients. Dry skin accentuates existing wrinkles, and thus an anti-aging ingredients may be beneficial.')
                else:
                    st.write('4. This product contains ***less than three*** anti-aging ingredients. If your skin tends to appear more wrinkly more anti-aging ingredients may be beneficial.')
            else:
                st.write('4. This product contains no anti-aging ingredients, dry skin actively looks for products/ingredients that promote a **anti-aging** on the skin.')

        if skin_type == 'Oily':
            st.markdown('''Here\'s how these ingredients may affect dry skin:            
            ''')

            contains_oil_c = 'oil control' in merged_dict.keys()
            if contains_oil_c:
                lots_of_oil_c = merged_dict['oil control'] > 2
                if lots_of_oil_c:
                    st.write('1. This product contains ***three or more*** oil controlling ingredients, beneficial to helping you control some of the excess oils that your skin produces.')
                else:
                    st.write('1. This product contains ***less than three*** oil controlling ingredients. If your skin tends to be on the more oilier side, more oil controlling ingredients may be beneficial.')
            else:
                st.write('1. This product contains no oil controlling ingredients, oily skin actively looks for products/ingredients that promote **oil control** and **pore minimization** to the skin. Looking for products that have more oil controlling ingredients may be beneficial.')

            contains_blackhead_r = 'blackhead reducing' in merged_dict.keys()
            if contains_blackhead_r:
                lots_of_blackhead_r = merged_dict['blackhead reducing'] > 2
                if lots_of_blackhead_r:
                    st.write('2. This product contains ***three or more*** blackhead reducing ingredients, beneficial to helping you reduce the number of unwanted blackheads that often arise from oily skin.')
                else:
                    st.write('2. This product contains ***less than three*** blackhead reducing ingredients. If your skin tends to be on the more oilier side, more blackhead reducing ingredients may be beneficial.')
            else:
                st.write('2. This product contains no blackhead reducing ingredients, oily skin actively looks for products/ingredients that promote **oil control** and **pore minimization** to the skin. Acne may also be a common unwanted issue with oily skin, and thus looking for products that have more blackhead reducing ingredients may be beneficial.')

            contains_pore_r = 'pore minimizer' in merged_dict.keys()
            if contains_pore_r:
                lots_of_pore_r = merged_dict['pore minimizer'] > 2
                if lots_of_pore_r:
                    st.write('3. This product contains ***three or more*** pore minimizing ingredients, beneficial to helping reduce the size of pores on your skin, which may be helpful in reducing the oily look of your skin.')
                else:
                    st.write('3. This product contains ***less than three*** pore minimizing ingredients. If your skin tends to be on the more oilier side, more pore reducing ingredients may be beneficial.')
            else:
                st.write('3. This product contains no pore minimizing ingredients, oily skin actively looks for products/ingredients that promote **oil control** and **pore minimization** to the skin. Looking for products that have more pore minimizing ingredients may be beneficial.')

            contains_hydratio = 'hydration' in merged_dict.keys()
            if contains_hydratio:
                lots_of_hydratio = merged_dict['hydration'] > 2
                if lots_of_hydratio:
                    st.write('4. This product contains ***three or more*** hydrating ingredients. While you still want hydration, you want to ensure that you are not overly hydrating the skin, and you may want a product with less hydrating ingredients.')
                else:
                    st.write('4. This product contains ***less than three*** hydrating ingredients. If your skin tends to be on the more oilier side, less hydrating ingredients is better.')
            else:
                st.write('4. This product contains no hydrating ingredients. While oily skin requires less hydrating ingredients than dry skin, oily skin can still benefit from some hydrating ingredients.')

            contains_acne = 'anti-acne' in merged_dict.keys()
            if contains_acne:
                lots_of_acne = merged_dict['anti-acne'] > 2
                if lots_of_acne:
                    st.write(
                        '5. This product contains ***three or more*** anti-acne ingredients, helping reduce the likelihood of developing acne that may be more apparent on oily skin.')
                else:
                    st.write('5. This product contains ***less than three*** pore minimizing ingredients. If your skin tends to be on the more oilier side, then you may be more susceptible to acne, and thus you may want to consider a product with more anti-acne ingredients.')
            else:
                st.write('5. This product contains no anti-acne ingredients. Oily skin tends to be more susceptible to acne, and thus you may want to consider a product with anti-acne ingredients.')

        if skin_type == 'Combination':
            st.markdown('''Below is a general overview of some of the benefits associated with these ingredients. Please note that combination skin varies and should consider your own skin with the purported benefits           
            ''')
            contains_oil_c = 'oil control' in merged_dict.keys()
            if contains_oil_c:
                lots_of_oil_c = merged_dict['oil control'] > 2
                if lots_of_oil_c:
                    st.write('1. This product contains ***three or more*** oil controlling ingredients. If your skin is on the oilier side, then oil control may be beneficial to helping you control some of the excess oils that your skin produces. If your skin is on the drier side, you may want to avoid oil control as your skin may be lacking in natural oils.')
                else:
                    st.write('1. This product contains ***less than three*** oil controlling ingredients. If your skin tends to be on the more oilier side, more oil controlling ingredients may be beneficial. Depending on how dry your skin is, you may enjoy less oil control, as the more dry your skin is the less natural oils there are')
            else:
                st.write('1. This product contains no oil controlling ingredients. If your skin is on the oilier side, then you may want a product with more oil control. If your skin is on the drier side, then you may want to avoid more oil control.')

            contains_blackhead_r = 'blackhead reducing' in merged_dict.keys()
            if contains_blackhead_r:
                lots_of_blackhead_r = merged_dict['blackhead reducing'] > 2
                if lots_of_blackhead_r:
                    st.write('2. This product contains ***three or more*** blackhead reducing ingredients, beneficial to helping you reduce the number of unwanted blackheads that often arise from oily skin. If your skin is on the drier side, blackhead reducing ingredients may dry your skin, and you may want to use blackhead reduction only when necessary.')
                else:
                    st.write('2. This product contains ***less than three*** blackhead reducing ingredients. If your skin tends to be on the more oilier side, more blackhead reducing ingredients may be beneficial. If you have drier skin but still have blackheads, you may want a smaller number of ingredients that reduce blackheads.')
            else:
                st.write('2. This product contains no blackhead reducing ingredients, oily skin actively looks for products/ingredients that promote **oil control** and **pore minimization** to the skin. Acne may also be a common unwanted issue with oily skin, and thus looking for products that have more blackhead reducing ingredients may be beneficial. If your skin is on the drier side but you still have blackheads, you may want to look for a product with some blackhead reducing ingredients but not too much.')

            contains_pore_r = 'pore minimizer' in merged_dict.keys()
            if contains_pore_r:
                lots_of_pore_r = merged_dict['pore minimizer'] > 2
                if lots_of_pore_r:
                    st.write('3. This product contains ***three or more*** pore minimizing ingredients, beneficial to helping reduce the size of pores on your skin, which may be helpful in reducing the oily look of your skin. If your skin is on the drier side, you may want to avoid pore minimizers, as your skin may be lacking in natural oils.')
                else:
                    st.write('3. This product contains ***less than three*** pore minimizing ingredients. If your skin tends to be on the more oilier side, more pore reducing ingredients may be beneficial. If your skin is on the drier side, you may want to avoid pore minimization depending on how dry your skin is.')
            else:
                st.write('3. This product contains no pore minimizing ingredients, oily skin actively looks for products/ingredients that promote **oil control** and **pore minimization** to the skin. Looking for products that have more pore minimizing ingredients may be beneficial. If you have drier skin, then you may want to avoid products with pore minimization.')

            contains_hydratio = 'hydration' in merged_dict.keys()
            if contains_hydratio:
                lots_of_hydratio = merged_dict['hydration'] > 2
                if lots_of_hydratio:
                    st.write('4. This product contains ***three or more*** hydrating ingredients. While you still want hydration, you want to ensure that you are not overly hydrating the skin, and you may want a product with less hydrating ingredients. If you have drier skin, you may benefit from  more hydrating ingredients.')
                else:
                    st.write('4. This product contains ***less than three*** hydrating ingredients. If your skin tends to be on the more oilier side, less hydrating ingredients is better. If your skin is on the drier side, you may benefit from a product with more hydrating ingredients.')
            else:
                st.write('4. This product contains no hydration ingredients. While oily skin requires less hydrating ingredients than dry skin, oily skin can still benefit from some hydrating ingredients. If your skin is drier, then you may need a product with hydrating ingredients.')

            contains_acne = 'anti-acne' in merged_dict.keys()
            if contains_acne:
                lots_of_acne = merged_dict['anti-acne'] > 2
                if lots_of_acne:
                    st.write('5. This product contains ***three or more*** anti-acne ingredients, helping reduce the likelihood of developing acne. If you have drier skin but still have acne, you may want a product that has less anti-acne ingredients.')
                else:
                    st.write('5. This product contains ***less than three*** pore minimizing ingredients. If your skin tends to be on the more oilier side, then you may be more susceptible to acne, and thus you may want to consider a product with more anti-acne ingredients. If your skin is on the drier side but you still need anti-acne ingredients, this product may be better as there are less anti-acne ingredients to cause further drying of the skin.')
            else:
                st.write('5. This product contains no anti-acne ingredients. Oily skin tends to be more susceptible to acne, and thus you may want to consider a product with anti-acne ingredients. If your skin is drier, then you may want to only seek out anti-acne ingredients when necessary.')

            # soothing helps lock in moisture
            contains_soothing = 'soothing' in merged_dict.keys()

            if contains_soothing:
                lots_of_soothing = merged_dict['soothing'] > 2
                if lots_of_soothing:
                    st.write('6. This product contains ***three or more*** soothing ingredients, beneficial to helping repair your skin barrier and inflammation that appear in dry skin. If you have oilier skin, then you may want to avoid too much soothing to avoid a build up of excessive oils.')
                else:
                    st.write('6. This product contains ***less than three*** soothing ingredients. If your skin tends to have inflammation and poor skin barrier, more soothing ingredients may be beneficial. If you have oily skin but still need a soothing product, then the less ingredients may be beneficial.')
            else:
                st.write('6. This product contains no soothing ingredients, dry skin actively looks for products/ingredients that promote a **healthy skin barrier**  to the skin. Looking for products that have more soothing ingredients may be beneficial. If your skin is oilier, then you may only want to use soothing ingredients when necessary.')
            # should go against oil control since dry skin lacks oil

            contains_aging = 'anti-aging' in merged_dict.keys()

            if contains_aging:
                lots_of_aging = merged_dict['anti-aging'] > 2
                if lots_of_aging:
                    st.write('7. This product contains ***three or more*** anti-aging ingredients. Dry skin accentuates existing wrinkles, and thus an anti-aging ingredients may be beneficial.')
                else:
                    st.write('7. This product contains ***less than three*** anti-aging ingredients. If your skin tends to appear more wrinkly more anti-aging ingredients may be beneficial.')
            else:
                st.write('7. This product contains no anti-aging ingredients, dry skin actively looks for products/ingredients that promote a **anti-aging** on the skin.')

        if skin_type == 'Sensitive':
            st.markdown('''With sensitive skin it is better to be cautious when approaching a product as there may be many different underlying factors to take into account. When in doubt, a dermatologist should be contacted about a product, as sensitive skin may potentially negatively react with various ingredients and/or products.            
            ''')

            contains_hydration = 'hydration' in merged_dict.keys()

            if contains_hydration:
                st.write('1. This product contains hydrating ingredients. With sensitive skin, hydrating products ***may*** be beneficial, as dry skin may be a symptom depending on whatever is causing your sensitive skin.')
            else:
                st.write('1. This product contains no hydrating ingredients. If dryness is a symptom of your sensitive skin, then you ***may*** benefit from using hydrating ingredients')

            contains_aging = 'soothing' in merged_dict.keys()

            if contains_aging:
                st.write('2. This product contains soothing ingredients. If you believe inflammation may be a result of sensitive skin, then soothing ingredients ***may*** be beneficial to you.')
            else:
                st.write('2. This product contains no soothing ingredients. If you believe that inflammation is a result of your sensitive skin, then you ***may*** benefit from a product that soothes the skin.')

            contains_spots = 'dark spot fading' in merged_dict.keys()

            if contains_spots:
                st.write('3. This product contains dark spot fading ingredients. If you find dark spots on your skin, then dark spot fading products ***may*** be beneficial to you')
            else:
                st.write('3. There are no dark spot fading ingredients. If dark spots are a symptom for you, then you ***may*** benefit from dark spot fading ingredients.')

            contains_even = 'evens skin tone' in merged_dict.keys()

            if contains_even:
                st.write('4. This product contains ingredients that may even your skin tone. If you find that uneven skin tones are a result of your sensitive skin, then you ***may*** benefit from these ingredients')
            else:
                st.write('4. This product does not contain ingredients that may even your skin tone. If you find that uneven skin tones are a result of your sensitive skin, then you ***may*** benefit from ingredients that even out your skin tone.')
if butt_2:
    if len(options) != 0:
        st.write('#### What Are The Ingredients\' Background?')
    else:
        st.write('Please select what you care about in your cosmetic products')
    if 'Cruelty-Free/Vegan' in options:
        st.write('##### Cruelty-Free/Vegan Ingredient Breakdown:')
        yes = (ingred_info_df.is_vegan_friendly.value_counts(
            normalize=True) * 100).round(2)
        idx = yes.index
        val = yes.values
        for i in range(len(yes)):
            st.write(
                f'**{val[i]}%** of the found ingredients are confirmed **"{idx[i]}"** to be vegan')
            if idx[i] == 'yes':
                st.write('**Ingredients include:** ' + ", ".join(
                    ingred_info_df[ingred_info_df.is_vegan_friendly == idx[i]].ingredient))

            if idx[i] != 'yes':
                df = ingred_info_df[ingred_info_df.is_vegan_friendly == idx[i]]
                # print('_______________________________________')
                for j in range(df.shape[0]):
                    st.write(
                        f'**Ingredient:** {df.ingredient.iloc[j]}; **Reason:** {df.not_vegan_reason.iloc[j]}')
            st.write('___________________________________________________________________')

    if 'Pretroleum-Free' in options:
        st.write('##### Petroleum-based Ingredient Breakdown:')
        yes = (ingred_info_df.petroleum_oil_based.value_counts(
        normalize=True) * 100).round(2)
        idx = yes.index
        val = yes.values
        for i in range(len(yes)):
            st.write(
                f'**{val[i]}%** of the found ingredients are confirmed **"{idx[i]}"** to be pretroleum-based')
            st.write('**Ingredients include:** ' + ", ".join(
                ingred_info_df[ingred_info_df.petroleum_oil_based == idx[i]].ingredient))
            st.write('___________________________________________________________________')

    if 'Mineral-Free' in options:
        st.write('##### Mineral-based Ingredient Breakdown:')
        yes = (ingred_info_df.mineral_based.value_counts(
        normalize=True) * 100).round(2)
        idx = yes.index
        val = yes.values
        for i in range(len(yes)):
            st.write(
                f'**{val[i]}%** of the found ingredients are confirmed **"{idx[i]}"** to be mineral-based')
            st.write('**Ingredients include:** ' + ", ".join(
                ingred_info_df[ingred_info_df.mineral_based == idx[i]].ingredient))
            st.write('___________________________________________________________________')

    if 'Paraben-Free' in options:
        st.write('##### Paraben-based Ingredient Breakdown:')
        yes = (ingred_info_df.paraben_based.value_counts(
        normalize=True) * 100).round(2)
        idx = yes.index
        val = yes.values
        for i in range(len(yes)):
            st.write(
                f'**{val[i]}%** of the found ingredients are confirmed **"{idx[i]}"** to be paraben-based')
            st.write('**Ingredients include:** ' + ", ".join(
                ingred_info_df[ingred_info_df.paraben_based == idx[i]].ingredient))
            st.write('___________________________________________________________________')

    if 'Fragrance-Free' in options:
        st.write('##### Fragrance-based Ingredient Breakdown:')
        yes = (ingred_info_df.paraben_based.value_counts(
        normalize=True) * 100).round(2)
        idx = yes.index
        val = yes.values
        for i in range(len(yes)):
            st.write(
                f'**{val[i]}%** of the found ingredients are confirmed **{idx[i]}** to be fragrance-based')
            st.write('**Ingredients include:** ' + ", ".join(
                ingred_info_df[ingred_info_df.paraben_based == idx[i]].ingredient))
            st.write('___________________________________________________________________')

    if 'Natural Ingredients' in options:
        st.write('##### Natural/Synthetic Ingredient Breakdown:')
        yes = (ingred_info_df.is_synthetic.value_counts(
        normalize=True) * 100).round(2)
        idx_1 = yes.index
        idx = ['Synthetic','Natural']
        val = yes.values
        for i in range(len(yes)):
            st.write(
                f'**{val[i]}%** of the found ingredients are confirmed **{idx[i]}** ingredients')
            st.write('**Ingredients include:** ' + ", ".join(
                ingred_info_df[ingred_info_df.is_synthetic== idx_1[i]].ingredient))
            st.write('___________________________________________________________________')

if butt_3:
    st.write('#### What Ingredients Appear to Have Risks?')
    yuh = ingred_info_df[ingred_info_df.web.notna()]
    if yuh.shape[0] > 0:
        st.write('##### Ingredient Proposed Risks According to Online Resources:')
    else:
        st.write('No ingredients were found to have proposed risks')
    for i in range(len(yuh)):
        st.write(f'###### **{yuh.ingredient.iloc[i]}**')
        
        websites = yuh.web.iloc[i].split(', ')
        for j in range(len(websites)):
            st.write(f'{websites[j]}')
        ha = ingred_info_df[ingred_info_df.cunt.notna()]
        if yuh.ingredient.iloc[i] in ha.ingredient.values:
            st.write(f'This ingredient is found to have restrctions in these regions: {ha[ha.ingredient == yuh.ingredient.iloc[i]].cunt.iloc[0]}')
        st.write('___________________')


if butt_4:
    benefit_count = ingred_info_df['function'].dropna(
    ).str.split(', ').apply(Counter).reset_index(drop=True)
    list_of_dicts = list(benefit_count)
    merged_dict = {}
    for dict in list_of_dicts:
        for key, value in dict.items():
            if key in merged_dict:
                merged_dict[key] += value
            else:
                merged_dict[key] = value
    if len(ingred_info_df['function'].dropna(
    )) > 0:
        st.write('##### What Are The Ingredients\' Functions?')
    for (key, value) in merged_dict.items():
        ingred_list = ingred_info_df[ingred_info_df['function'].fillna(
            'None').str.contains(key)]['ingredient']
        st.markdown(f'''There were **{str(value)} ingredient(s)** that function as **{str(key)}**:    
        {', '.join(str(x) for x in list(ingred_list))}
        ''')
        st.write("____")


