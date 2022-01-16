from sentence_transformers import SentenceTransformer, util
import db
import scipy

def get_most_similar(user_input):
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    training_data = db.get_all_training_data()
    # 製作辭庫
    sentences_list = [sen[0] for sen in training_data]
    print(sentences_list)
    sentence_embeddings = model.encode(sentences_list)
    # input question
    query_embedding = model.encode([user_input])

    print(sentence_embeddings.shape)
    # 與資料庫計算consin相似度
    distances = scipy.spatial.distance.cdist([query_embedding[0]], sentence_embeddings, "cosine")[0]
    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])
    idx, distance = results[0]
    print(training_data[idx], "(Cosine Score: %.4f)" % (1 - distance))

    return training_data[idx], 1-distance

if __name__=="__main__":
    get_most_similar("開寶箱")
