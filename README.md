# Consumer-Neutral-Approach-to-Cosmetic-Safety

## Skincare Ingredients Breakdown
<b> <font size="3.5">Introduction </font><b>

<font size="2">Skincare has blown up throughout the past recent years and has been a big topic flowing around the internet. We can see an increase in discussions online (Reddit, Youtube, Tiktok) about what products are bad and good for your skin, yet we are left with vague and inconsistent answers that don't really help us gauge if we should using specific cosmetic products. However, organization such as EWG's Skin Deep database have found a way to give consumers a deeper look on their skincare products/ingredients through assessing their own scale of skincare "safeness".</font>

<font size="2">The potential issue with databases such as EWG's is that there tends to be an overestimate on the dangers of specific ingredients and EWG has even been coined as a "fear-mongering" campaign by many. EWG assess the safeness based off of scientific papers, noting of an ingredient's potential hazards such as toxicity and allergies. Sometimes, these hazard ratings can be based off of scientific suspicions of certain ingredients that have happened and can cause certain products to be thrown in the dust due to these safeness ratings.</font>

<font size="2">It's difficult to find this "perfect balance" of what is good and bad and also have it truthfully represent how everyone views cosmetic ingredients. Although there are generally well-known harmful ingredients to avoid, it's almost impossible to sort through thousands of different ingredients that exist today and do extensive research to reach a point of confidence to coin whether a product/ingredient is harzardous or not.</font>

<b><font size="3.5"> Approach </font> <b>
    
<font size="2.5">Instead of having to resort to resources online that may or may not be credible, we decided to approach this issue by allowing cosmetic product consumers to decide on their own what they believe is "good" or "useful" in terms of their skin. We wanted to provide breakdowns of skincare products and their ingredients in a more neutral manner, providing informational breakdown on where ingredients come from and how each product may benefit them.</font>
    
<font size="2">Although this shouldn't be a replacement for ingredient research that has credentials, it can provide consumers with a lot less stress on having to navigating every ingredient they have or will use.</font>

<b><font size="3.5"> Dataset Breakdown/How was this Collected? </font> <b>
    
Here are the column breakdown for this dataset:

* **`ingredient`** : the name of the ingredient
* **`is_vegan_friendly`** : is it fully vegan friendly? "maybe" can occur if an ingredient can possibly be non-vegan depending on how it was made
* **`not_vegan_reason`** : reason why the ingredient isn't vegan or might not be vegan
* **`petroleum_oil_based`** : is it a petroleum based ingredient?
* **`plant_oil_based`** : is it a plant oil based ingredient?
* **`mineral_based`** : is it a mineral based ingredient?
* **`plant_nonoil_based`** : is it a plant-based ingredient (not including plant-based oils)?
* **`animal_based`** : is it a animal based product?
* **`paraben_based`** : is it a paraben based ingredient?
* **`fragrance_based`** : is it a fragrance based ingredient?
* **`is_synthetic`** : is this ingredient synethically produced?
* **`is_natural`** : does this ingredient naturally occur?
* **`function`** : proposed function based off of [Paula's Choice Ingredient Dictionary](https://www.paulaschoice.com/ingredient-dictionary)
* **`proposed_risks`** : Does this ingredient have any studyies or research that show potential risks?
* **`known_benefits`** : proposed benefits based off of [Paula's Choice Ingredient Dictionary](https://www.paulaschoice.com/ingredient-dictionary)
* **`other_names`** : other names this ingredient might go under taken from [EWG's skin deep](https://www.ewg.org/skindeep/) 

**NOTE - most of these columns were produced through research on each individual ingredient**
