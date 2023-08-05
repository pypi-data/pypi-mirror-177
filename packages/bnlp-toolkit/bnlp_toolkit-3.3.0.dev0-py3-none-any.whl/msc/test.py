from bnlp import BengaliDoc2vec
bd = BengaliDoc2vec()

def test_vector_gen():
    model_path = "msc/news_article_doc2vec/bangla_news_article_doc2vec.model"
    text = "রাষ্ট্রবিরোধী ও উসকানিমূলক বক্তব্য দেওয়ার অভিযোগে গাজীপুরের গাছা থানায় ডিজিটাল নিরাপত্তা আইনে করা মামলায় আলোচিত ‘শিশুবক্তা’ রফিকুল ইসলামের বিরুদ্ধে অভিযোগ গঠন করেছেন আদালত। ফলে মামলার আনুষ্ঠানিক বিচার শুরু হলো। আজ বুধবার (২৬ জানুয়ারি) ঢাকার সাইবার ট্রাইব্যুনালের বিচারক আসসামছ জগলুল হোসেন এ অভিযোগ গঠন করেন। এর আগে, রফিকুল ইসলামকে কারাগার থেকে আদালতে হাজির করা হয়। এরপর তাকে নির্দোষ দাবি করে তার আইনজীবী শোহেল মো. ফজলে রাব্বি অব্যাহতি চেয়ে আবেদন করেন। অন্যদিকে, রাষ্ট্রপক্ষ অভিযোগ গঠনের পক্ষে শুনানি করেন। উভয় পক্ষের শুনানি শেষে আদালত অব্যাহতির আবেদন খারিজ করে অভিযোগ গঠনের মাধ্যমে বিচার শুরুর আদেশ দেন। একইসঙ্গে সাক্ষ্যগ্রহণের জন্য আগামী ২২ ফেব্রুয়ারি দিন ধার্য করেন আদালত।"

    vector = bd.get_document_vector(model_path, text)
    print(vector)

def test_document_similarity():
    model_path = "msc/news_article_doc2vec/bangla_news_article_doc2vec.model"
    text = "রাষ্ট্রবিরোধী ও উসকানিমূলক বক্তব্য দেওয়ার অভিযোগে গাজীপুরের গাছা থানায় ডিজিটাল নিরাপত্তা আইনে করা মামলায় আলোচিত ‘শিশুবক্তা’ রফিকুল ইসলামের বিরুদ্ধে অভিযোগ গঠন করেছেন আদালত। ফলে মামলার আনুষ্ঠানিক বিচার শুরু হলো। আজ বুধবার (২৬ জানুয়ারি) ঢাকার সাইবার ট্রাইব্যুনালের বিচারক আসসামছ জগলুল হোসেন এ অভিযোগ গঠন করেন। এর আগে, রফিকুল ইসলামকে কারাগার থেকে আদালতে হাজির করা হয়। এরপর তাকে নির্দোষ দাবি করে তার আইনজীবী শোহেল মো. ফজলে রাব্বি অব্যাহতি চেয়ে আবেদন করেন। অন্যদিকে, রাষ্ট্রপক্ষ অভিযোগ গঠনের পক্ষে শুনানি করেন। উভয় পক্ষের শুনানি শেষে আদালত অব্যাহতির আবেদন খারিজ করে অভিযোগ গঠনের মাধ্যমে বিচার শুরুর আদেশ দেন। একইসঙ্গে সাক্ষ্যগ্রহণের জন্য আগামী ২২ ফেব্রুয়ারি দিন ধার্য করেন আদালত।"
    sim = bd.get_document_similarity(model_path, text, text)
    print(sim)

def train_model():
    text_files = "msc/files"
    checkpoint_path = "msc/logs"
    bd.train_doc2vec(text_files, checkpoint_path=checkpoint_path)

def test_spacy_tokenizer():
    from bnlp.tokenizer.spacy import spacy_tokenizer
    text = "আমি বাংলায় গান গাই."
    tokens = spacy_tokenizer(text)
    print(tokens)

def test_spacy_ner():
    from bnlp.ner import spacy_ner
    text = "মো. নাহিদ হুসাইন নামের এক পরীক্ষার্থী অভিযোগ করেন, ইডেন মহিলা কলেজের পাঠাগার ভবনের দ্বিতীয় তলায় তাঁর পরীক্ষার আসন ছিল।"
    model_path = "msc/spacy_bn_model/output/model-best"
    output = spacy_ner(text, model_path)
    print(output)
    # [
    #     {'text': 'নাহিদ হুসাইন', 'label': 'PER', 'start_char': 4, 'end_char': 16, 'start_token': 1, 'end_token': 3}, 
    #     {'text': 'পরীক্ষার্থী', 'label': 'PER', 'start_char': 26, 'end_char': 37, 'start_token': 5, 'end_token': 6}, 
    #     {'text': 'মহিলা কলেজের', 'label': 'ORG', 'start_char': 56, 'end_char': 68, 'start_token': 10, 'end_token': 12}, 
    #     {'text': 'তাঁর', 'label': 'PER', 'start_char': 98, 'end_char': 102, 'start_token': 16, 'end_token': 17}
    # ]


if __name__ == "__main__":
    # test_vector_gen()
    # test_document_similarity()
    # train_model()
    # test_spacy_tokenizer()
    test_spacy_ner()