from __future__ import division
import string
import math
import csv

tokenize = lambda doc: doc.lower().split(" ")

#doc1: from webmd, connecting word is triggered
document_0 = "Sinusitis is an inflammation, or swelling, of the tissue lining the sinuses. Normally, sinuses are filled with air, but when sinuses become blocked and filled with fluid, germs (bacteria, viruses, and fungi) can grow and cause an infection."

#doc2: from wikipedia, connecting word is the same as webmed
document_1 = "Common allergens include pollen and food. Metals and other substances may also cause problems.[1] Food, insect stings, and medications are common causes of severe reactions. Their development is due to both genetic and environmental factors.[6] The underlying mechanism involves immunoglobulin E antibodies (IgE), part of the body's immune system, binding to an allergen and then to a receptor on mast cells or basophils where it triggers the release of inflammatory chemicals such as histamine.[7] Diagnosis is typically based on a person's medical history. Further testing of the skin or blood may be useful in certain cases.[5] Positive tests, however, may not mean there is a significant allergy to the substance in question."
document_2 = "Many allergens such as dust or pollen are airborne particles. In these cases, symptoms arise in areas in contact with air, such as eyes, nose, and lungs. For instance, allergic rhinitis, also known as hay fever, causes irritation of the nose, sneezing, itching, and redness of the eyes.[18] Inhaled allergens can also lead to increased production of mucus in the lungs, shortness of breath, coughing, and wheezing."
#document_3 = "Vladimir Putin is working hard to fix the economy in Russia as the Ruble has tumbled."
#document_4 = "What's the future of Abenomics? We asked Shinzo Abe for his views"
#document_5 = "Obama has eased sanctions on Cuba while accelerating those against the Russian Economy, even as the Ruble's value falls almost daily."
#document_6 = "Vladimir Putin is riding a horse while hunting deer. Vladimir Putin always seems so serious about things - even riding horses. Is he crazy?"

#all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]
all_documents=[document_0, document_1,document_2]
def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document))/max_count))

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

#in Scikit-Learn




########### END BLOG POST 1 #############

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude


#This gets an array of documents. query[0] is always the one to see the similalrity against the rest of sentences. For example, query[0] is from 
#webmd article in keyword 'causes' then from query[1] - query[length-1] will have sentences that are all from wikipedia for the same keywords
from sklearn.feature_extraction.text import TfidfVectorizer
def compare(query,breakpoint):
    all_documents=query
    
    tfidf_representation = tfidf(all_documents)
    
    our_tfidf_comparisons = []

    sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
    sklearn_representation = sklearn_tfidf.fit_transform(all_documents)

    
    tdidf_csv=open('tdidf_result.csv','wb')

    print "tfidf"
    tdidf_count=0
    
    for count_0, doc_0 in enumerate(tfidf_representation):
        if (count_0 < breakpoint):
            for count_1, doc_1 in enumerate(tfidf_representation):
                if (count_1 >= breakpoint):
                    cos_sim=round(cosine_similarity(doc_0, doc_1),4)
                    if (cos_sim > 0.1):
                        tdidf_count += 1
                    print (cos_sim, count_0, count_1)
                    our_tfidf_comparisons.append((cos_sim, count_0, count_1))
    print "The number of cosine similarity above 0.1 is: " + str(tdidf_count)

    sklearn_count=0
    skl_tfidf_comparisons = []
    print "SKlearn"
    for count_0, doc_0 in enumerate(sklearn_representation.toarray()):
        if (count_0 < breakpoint):
            for count_1, doc_1 in enumerate(sklearn_representation.toarray()):
                if (count_1 >= breakpoint):
                    cos_sim=round(cosine_similarity(doc_0, doc_1),4)
                    if (cos_sim > 0.1):
                        sklearn_count += 1
                    print (cos_sim, count_0, count_1)
                    skl_tfidf_comparisons.append((cos_sim, count_0, count_1))
    print "The number of cosine similarity above 0.1 is: " + str(tdidf_count)
    print "\n"






