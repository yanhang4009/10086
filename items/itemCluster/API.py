from transformers import AutoTokenizer, BertModel
import torch
import pandas as pd
import numpy as np
import time

bert_path = "items/itemCluster/demo/AAAbertchinese"


def retrieve_headers(path):
  # 将一个csv文件中的header提取出来
  try:
    df = pd.read_csv(path, encoding='gbk', header=None, low_memory=False)
  except:
    return []
  else:
    return [str(ii) for ii in df.iloc[0]]
  
def API(file_path):
    """
    input: 
        file_path:想要处理的csv文件的路径
    output:
        output[0]:修改前的信息项名称
        output[1]:修改后的信息项名称
    """

    a1 = time.perf_counter()
    consolidated_item_path = './items/itemCluster/demo/items.txt'
    # with open(consolidated_item_path, 'r', encoding='gbk') as ppp:
    #     items = ppp.readlines()
    write_logits_path = './items/itemCluster/demo/logits.pt'
    headers = retrieve_headers(file_path)
    # logits_first_level = torch.load('/data/xrm/xrm/YiDong/yidong/demo/cluster_idx2logit.pt') # 每个元素是一个ndarray
    logits_first_level = torch.load('items/itemCluster/demo/cluster_idx2logit.pt') # 每个元素是一个ndarray
    # print('a?', type(logits_first_level[0]))
    # print(len(logits_first_level))
    # for iiii in logits_first_level:
       
    #    print(iiii.shape)
    
    # for idx, each_tensor in enumerate(logits_first_level):
    #     logits_first_level[idx] = each_tensor.numpy()
    # logits_first_level = np.array(logits_first_level)
    # all_consolidated_logits = torch.load(write_logits_path)
    # for idx, each_tensor in enumerate(all_consolidated_logits):
    #     all_consolidated_logits[idx] = each_tensor.numpy()
    a2 = time.perf_counter()
    tokenizer = AutoTokenizer.from_pretrained(bert_path)
    model = BertModel.from_pretrained(bert_path)
    data = tokenizer(headers, return_tensors="pt", truncation=True, padding='max_length', max_length=10)    
    
    print("headers: ", headers)
    with torch.no_grad():
        logits = model(**data)
    
    
        # if all_consolidated_logits[idx].shape != (5, 768):
        #     raise ValueError(f"样本点{idx}出现问题")

    # all_consolidated_logits = np.array(all_consolidated_logits)
    # logits_first_level = torch.stack(logits_first_level)
    logits_first_level = np.array(logits_first_level)
    # 这里写一个函数找最近就行了，然后通过下标去lines找对应的cluster，把这个cluter的第一项作为结果就好了
    a3 = time.perf_counter()
    # with open('demo/cluster_idx2id.txt', 'r') as pap:
    #     all_idx_in_each_cluster = dict(pap.read())

    original_list = []
    modified_list = []
    for idx, logit in enumerate(logits.last_hidden_state):
        numpy_logit = logit.numpy()[0]
        # print(numpy_logit.shape)
        differences = logits_first_level - numpy_logit 
        distances = np.linalg.norm(differences, axis=(1))  # 对 (5, 768) 维度求范数
        closest_cluster_index = np.argmin(distances)
        logit_file = 'items/itemCluster/demo/dividied_logits/cluster_logits_' + str(closest_cluster_index) + '.pt'
        items_file = 'items/itemCluster/demo/divided_items/items_' + str(closest_cluster_index) + '.txt'
        # print(logit_file)
        # print(closest_cluster_index)
        logits_second_level = torch.load(logit_file) # 每个元素是一个tensor
        # print('a?', type(logits_second_level[0]))
        # print('second_logit shape: ', logits_second_level.shape)
        # print(len(logits_second_level))
        logits_second_level = torch.stack(logits_second_level)
        # print('second_logit shape: ', logits_second_level.shape)
        logits_second_level = np.array(logits_second_level)
        # for idx, each_tensor in enumerate(logits_second_level):
            # logits_second_level[idx] = each_tensor.numpy()
        diff = logits_second_level - numpy_logit
        # print('second_logit shape: ', logits_second_level.shape)
        # print('diff shape: ', diff.shape)
        dist = np.linalg.norm(diff, axis=(1))  # 对 (5, 768) 维度求范数
        closest_index = np.argmin(dist)
        # break
    # print(type(items))
        # idx_in_this_cluster = all_idx_in_each_cluster[closest_cluster_index]
        # logits_in_this_cluster = ''
        # diff = 
        with open(items_file, 'r', encoding='gbk') as ppp:
            items = ppp.readlines()
        result = list(eval(items[closest_index]))
        if len(result) < 2:
            continue

        # TODO: 这里后续应该加一个if来判断什么情况下要修改
        original_list.append(headers[idx])
        # 这里选择下标1是因为不想和第一个重复（因为很有可能第一个我见过）但实际应用中应该可以重复
        modified_list.append(result[1])
        # print(result[0])
    print('original_list: ',original_list)
    print('modified_list: ',modified_list)
    a4 = time.perf_counter()
    print('读文件: ', a2-a1)
    print('bert处理: ',a3-a2)
    print('找最近: ', a4-a3)
    return original_list, modified_list  

if __name__=='__main__':
    print(API('法制宣传教育信息.csv'))    