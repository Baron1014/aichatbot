from transformers import AutoModel, BertTokenizer, BertConfig, BertForSequenceClassification
from torch.utils.data import DataLoader
from train import ActionDataset, create_mini_batch, inference, show_model_info
import pandas as pd
import torch

def state(test_df, PRETRAINED_MODEL_NAME, labels, NUM_LABELS=10):
    config = BertConfig.from_pretrained("models/bert", num_labels=NUM_LABELS)
    model = BertForSequenceClassification.from_pretrained("bert-base-chinese", config=config)
    model.load_state_dict(torch.load(f"{PRETRAINED_MODEL_NAME}/pytorch_model.bin"))
    # show_model_info(model)
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    predict_tag = testing(test_df, tokenizer, model, label=labels)
    # testing(test_df, tokenizer, model, label={'探索牆壁': 0, '探索畫框': 1, '無意義': 2})

    return predict_tag

def testing(test_df, tokenizer, model, label):
    # 建立測試集。
    testset = ActionDataset("test", test_df,tokenizer=tokenizer, label=label)

    testloader = DataLoader(testset, collate_fn=create_mini_batch)

    # 用分類模型預測測試集
    predictions = inference(model, testloader)
    # print(predictions)
    # 用來將預測的 label id 轉回 label 文字
    index_map = {v: k for k, v in testset.label_map.items()}
    # print(index_map)

    # 生成預測
    # df_pred = pd.DataFrame({"predict_tag": [index_map[i] for i in predictions.tolist()]})
    # final_df = pd.concat([test_df, df_pred], axis=1)
    # print(final_df)
    return [index_map[i] for i in predictions.tolist()][0]

if __name__ == "__main__":

    test_df = pd.DataFrame(data=[("房間燈光逐漸消失", "我要看畫")], columns=["robot", "user"])
    state(test_df, "models/bert", 3)
