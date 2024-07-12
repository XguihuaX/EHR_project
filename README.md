


**1: use other tools**

 ** 1.1 OPQRST parts**
 
  tools(metamap, ctakes, scisapcy) extraction conclusion: not suitable to engage OPQRST extraction tasks
  
  1 these tools rely on static libraries. However, OPQRST information is often expressed in a highly diverse way, resulting in these tools only being able to recognize a few of the relevant entities.
  
  2 These models face a challenge in OPQRST extraction tasks as they tend to extract all entities of the selected type. When dealing with longer electronic medical records, this often outputs tremendous irrelevant entities as long as belong to the target entity category. Due to a lack of contextual understanding, the models cannot further filter these entities, leading to highly redundant outputs. SciSpaCy can aid contextual understanding by creating custom NER templates combined with existing entity types; however, since custom entity types are static, it still does not solve the core issue.

  3: Recent studies using MetaMap and cTAKES for extracting information from electronic health records (EHR) have mostly focused on extracting relatively fixed entity types, such as symptoms, to do the classification tasks,  Only a few studies have combined machine learning and other methods into a pipeline to extract more complex information.
