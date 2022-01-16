import torch
import pandas as pd
from transformers import BertTokenizer
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn.utils.rnn import pad_sequence
# 載入一個可以做中文多分類任務的模型，n_class = 3
from transformers import BertForSequenceClassification
from sklearn.model_selection import train_test_split
import db

class ActionDataset(Dataset):
    # 讀取前處理後的 tsv 檔並初始化一些參數
    def __init__(self, mode, df, tokenizer, label):
        #assert mode in ["train", "test"]  # 一般訓練會需要 dev set
        self.mode = mode
        # 大數據會需要用 iterator=True
        #self.df = pd.read_csv(mode + ".tsv", sep="\t").fillna("")
        self.df = df
        self.len = len(self.df)
        self.label_map = label
        self.tokenizer = tokenizer  # 將使用 BERT tokenizer
    
    # 定義回傳一筆訓練 / 測試數據的函式
    def __getitem__(self, idx):
        if self.mode == "test":
            text_a, text_b = self.df.iloc[idx, :2].values
            label_tensor = None
        else:
            text_a, text_b, label = self.df.iloc[idx, :].values
            # 將 label 文字也轉換成索引方便轉換成 tensor
            label_id = self.label_map[label]
            label_tensor = torch.tensor(label_id)
            
        # 建立第一個句子的 BERT tokens 並加入分隔符號 [SEP]
        word_pieces = ["[CLS]"]
        tokens_a = self.tokenizer.tokenize(text_a)
        word_pieces += tokens_a + ["[SEP]"]
        len_a = len(word_pieces)
        
        # 第二個句子的 BERT tokens
        tokens_b = self.tokenizer.tokenize(text_b)
        word_pieces += tokens_b + ["[SEP]"]
        len_b = len(word_pieces) - len_a
        
        # 將整個 token 序列轉換成索引序列
        ids = self.tokenizer.convert_tokens_to_ids(word_pieces)
        tokens_tensor = torch.tensor(ids)
        
        # 將第一句包含 [SEP] 的 token 位置設為 0，其他為 1 表示第二句
        segments_tensor = torch.tensor([0] * len_a + [1] * len_b, 
                                        dtype=torch.long)
        
        return (tokens_tensor, segments_tensor, label_tensor)
    
    def __len__(self):
        return self.len


"""
定義一個可以針對特定 DataLoader 取得模型預測結果以及分類準確度的函式
"""
def inference(model, dataloader, compute_acc=False):
    predictions = None
    correct = 0
    total = 0
      
    with torch.no_grad():
        # 遍巡整個資料集
        for data in dataloader:
            # 將所有 tensors 移到 GPU 上
            if next(model.parameters()).is_cuda:
                data = [t.to("cuda:0") for t in data if t is not None]
            
            
            # 別忘記前 3 個 tensors 分別為 tokens, segments 以及 masks
            tokens_tensors, segments_tensors, masks_tensors = data[:3]
            outputs = model(input_ids=tokens_tensors, 
                            token_type_ids=segments_tensors, 
                            attention_mask=masks_tensors)
            
            logits = outputs[0]
            _, pred = torch.max(logits.data, 1)
            
            # # 用來計算訓練集的分類準確率
            # if compute_acc:
            #     labels = data[3]
            #     total += labels.size(0)
            #     correct += (pred == labels).sum().item()
                
            # 將當前 batch 記錄下來
            if predictions is None:
                predictions = pred
            else:
                predictions = torch.cat((predictions, pred))
    
    if compute_acc:
        acc = correct / total
        return predictions, acc
    return predictions

"""
定義一個可以針對特定 DataLoader 取得模型預測結果以及分類準確度的函式
"""
def get_predictions(model, dataloader, compute_acc=False):
    predictions = None
    correct = 0
    total = 0
      
    with torch.no_grad():
        # 遍巡整個資料集
        for data in dataloader:
            # 將所有 tensors 移到 GPU 上
            if next(model.parameters()).is_cuda:
                data = [t.to("cuda:0") for t in data if t is not None]
            
            
            # 別忘記前 3 個 tensors 分別為 tokens, segments 以及 masks
            tokens_tensors, segments_tensors, masks_tensors = data[:3]
            outputs = model(input_ids=tokens_tensors, 
                            token_type_ids=segments_tensors, 
                            attention_mask=masks_tensors)
            
            logits = outputs[0]
            _, pred = torch.max(logits.data, 1)
            
            # # 用來計算訓練集的分類準確率
            if compute_acc:
                labels = data[3]
                total += labels.size(0)
                correct += (pred == labels).sum().item()
                
            # 將當前 batch 記錄下來
            if predictions is None:
                predictions = pred
            else:
                predictions = torch.cat((predictions, pred))
    
    if compute_acc:
        acc = correct / total
        return predictions, acc
    return predictions
    


def create_mini_batch(samples):
    tokens_tensors = [s[0] for s in samples]
    segments_tensors = [s[1] for s in samples]
    
    # 測試集有 labels
    if samples[0][2] is not None:
        label_ids = torch.stack([s[2] for s in samples])
    else:
        label_ids = None
    
    # zero pad 到同一序列長度
    tokens_tensors = pad_sequence(tokens_tensors, 
                                  batch_first=True)
    segments_tensors = pad_sequence(segments_tensors, 
                                    batch_first=True)
    
    # attention masks，將 tokens_tensors 裡頭不為 zero padding
    # 的位置設為 1 讓 BERT 只關注這些位置的 tokens
    masks_tensors = torch.zeros(tokens_tensors.shape, 
                                dtype=torch.long)
    masks_tensors = masks_tensors.masked_fill(
        tokens_tensors != 0, 1)
    
    return tokens_tensors, segments_tensors, masks_tensors, label_ids
    
def show_process(trainset, tokenizer):
    # 選擇第一個樣本
    sample_idx = 0

    # 將原始文本拿出做比較
    text_a, text_b, label = trainset.df.iloc[sample_idx].values

    # 利用剛剛建立的 Dataset 取出轉換後的 id tensors
    tokens_tensor, segments_tensor, label_tensor = trainset[sample_idx]

    # 將 tokens_tensor 還原成文本
    tokens = tokenizer.convert_ids_to_tokens(tokens_tensor.tolist())
    combined_text = "".join(tokens)

    # 渲染前後差異，毫無反應就是個 print。可以直接看輸出結果
    print(f"""[原始文本]
    句子 1：{text_a}
    句子 2：{text_b}
    分類  ：{label}

    --------------------

    [Dataset 回傳的 tensors]
    tokens_tensor  ：{tokens_tensor}

    segments_tensor：{segments_tensor}

    label_tensor   ：{label_tensor}

    --------------------

    [還原 tokens_tensors]
    {combined_text}
    """)

def show_dataloader(trainloader):
    data = next(iter(trainloader))

    tokens_tensors, segments_tensors, masks_tensors, label_ids = data

    print(f"""
    tokens_tensors.shape   = {tokens_tensors.shape} 
    {tokens_tensors}
    ------------------------
    segments_tensors.shape = {segments_tensors.shape}
    {segments_tensors}
    ------------------------
    masks_tensors.shape    = {masks_tensors.shape}
    {masks_tensors}
    ------------------------
    label_ids.shape        = {label_ids.shape}
    {label_ids}
    """)

def show_model_info(model):
    print("""
    name            module
    ----------------------""")
    for name, module in model.named_children():
        if name == "bert":
            for n, _ in module.named_children():
                print(f"{name}:{n}")
        else:
            print("{:15} {}".format(name, module))
    print(model.config)

def train(model, trainloader, device, EPOCHS = 100):
    # 訓練模式
    model.train()

    # 使用 Adam Optim 更新整個分類模型的參數
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)


    for epoch in range(EPOCHS):
        
        running_loss = 0.0
        for data in trainloader:
            
            tokens_tensors, segments_tensors, \
            masks_tensors, labels = [t.to(device) for t in data]

            # 將參數梯度歸零
            optimizer.zero_grad()
            
            # forward pass
            outputs = model(input_ids=tokens_tensors, 
                            token_type_ids=segments_tensors, 
                            attention_mask=masks_tensors, 
                            labels=labels)

            loss = outputs[0]
            # backward
            loss.backward()
            optimizer.step()


            # 紀錄當前 batch loss
            running_loss += loss.item()
            
        # 計算分類準確率
        _, acc = get_predictions(model, trainloader, compute_acc=True)

        print('[epoch %d] loss: %.3f, acc: %.3f' %
            (epoch + 1, running_loss, acc))

    return model

def testing(test_df, tokenizer, model, label):
    # 建立測試集。
    testset = ActionDataset("test", test_df,tokenizer=tokenizer, label=label)

    testloader = DataLoader(testset,
                            collate_fn=create_mini_batch)

    # 用分類模型預測測試集
    predictions = get_predictions(model, testloader)
    print(predictions)
    # 用來將預測的 label id 轉回 label 文字
    index_map = {v: k for k, v in testset.label_map.items()}

    # 生成預測
    df_pred = pd.DataFrame({"predict_tag": [index_map[i] for i in predictions.tolist()]})
    final_df = pd.concat([test_df, df_pred], axis=1)
    print(final_df)

def preprocess_training(df, NUM_LABELS, BATCH_SIZE, label):
    #train_df, test_df = train_test_split(df, test_size=0.1)
    #print(test_df)
    # 初始化一個專門讀取訓練樣本的 Dataset，使用中文 BERT 斷詞
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    trainset = ActionDataset("train", df, tokenizer=tokenizer, label=label)
    show_process(trainset, tokenizer)
    # 利用 `collate_fn` 將 list of samples 合併成一個 mini-batch 是關鍵
    trainloader = DataLoader(trainset, batch_size=BATCH_SIZE, collate_fn=create_mini_batch)
    show_dataloader(trainloader)
    model = BertForSequenceClassification.from_pretrained("bert-base-chinese", num_labels=NUM_LABELS)
    show_model_info(model)
    # 讓模型跑在 GPU 上並取得訓練集的分類準確率
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device:", device)
    model = model.to(device)
    _, acc = get_predictions(model, trainloader, compute_acc=True)
    print("classification acc:", acc)
    # 訓練模型
    model = train(model, trainloader, device)
    # testing
    testing(df, tokenizer, model, label=label)

    return model, tokenizer

def bert(NUM_LABELS = 10, BATCH_SIZE = 32, label={'探索牆壁': 0, '探索畫框': 1, '無意義': 2}):
#     wall=[
#   ["那裡有面大大的牆壁", "探索它", "探索牆壁"],
#   ["那裡有個一面白的牆壁", "查看它", "探索牆壁"],
#   ["有面牆壁", "敲敲它", "探索牆壁"],
#   ["什麼!?好像是牆壁", "上面有東西嗎？", "探索牆壁"],
#   ["牆壁上什麼都沒有", "再仔細看看", "探索牆壁"],
#   ["你接下來要做什麼", "看看牆上有無東西", "探索牆壁"],
#   ["這個空間裡四面八方環繞乾淨的牆", "看牆壁有沒有東西", "探索牆壁"]
#   ]

#     nothing=[
#         ["那裡有個又大又白的牆壁", "無視它", "無意義"],
#         ["那裡有個又大又白的牆壁", "好喔", "無意義"],
#         ["有隻狗跟一根雞腿", "吃雞腿", "無意義"],
#         ["牆上有一幅畫", "掉頭而去", "無意義"],
#         ["牆上有一幅畫", "躺下", "無意義"],
#         ["有一幅畫欸", "去看寶箱", "無意義"],
#         ["牆上有個東西", "螞蟻嗎?", "無意義"]
#         ]

#     painting=[
#         ["牆上似乎有個東西", "是什麼?", "探索畫框"],
#         ["牆上好像有個五顏六色的東西", "是畫嗎?", "探索畫框"],
#         ["牆上有個你看不懂得塗鴉", "把它翻過來看", "探索畫框"],
#         ["你發現畫時感覺好像跟一般畫不一樣", "翻過來看", "探索畫框"],
#         ["接下來你要做什麼呢?", "把畫翻過來", "探索畫框"],
#         ["有一幅畫欸", "背後有東西嗎", "探索畫框"]
#     ]

    entity_list = db.get_bert_training_data()
    label_entity_list = db.get_all_labels()
    training_data = [[state, ui, tag]for state, ui, tag in entity_list]
    labels = {tag: t_id-1 for t_id, tag in label_entity_list}
    print(labels)

    df = pd.DataFrame(training_data, columns=["state", "user", "tag"])
    model, token = preprocess_training(df, NUM_LABELS, BATCH_SIZE, label=labels)
    # save model
    model.save_pretrained('models/bert')


if __name__=="__main__":
    bert(NUM_LABELS=14)
