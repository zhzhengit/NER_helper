import json
import re
punctuation = ",\"!?:'"

def span2bio(input_dir, output_dir):
    """
    span —> bio format
	Args:
		[
            {"context": "",
		    "label": {
            "entity1": "organisation",
            "entity2": "location",
            "entity3": "MISC" }
            },
            ....
        ]
    """
    f_write=open(output_dir,"w")

    file = open(input_dir, 'r')
    js = file.read()
    dic = json.loads(js)
    data_length = (len(dic))
    context_len = 0
    for i in range(data_length):
        data = dic[i]
        context = data['context']
        label = data['label']
        new_label={}
        
        count_lsit = []

        
        for p in punctuation:
            context = context.replace(p, " "+p) 
        context = re.sub('.$', ' .', context)   
        context = context.split(' ')
        context_len += len(context)
        line_len = 0
        for idx in (context):
            label_list = []
            word_list = []
            idx = idx.replace('\n','')
            for key in label.keys():
                ori_key = key
                for p in punctuation:
                    key = key.replace(p, " "+p) 
                key1 = key.split(' ')
                if len(key1)>=2:
                    count = 0
                # print(label[key])
                    for idy in key1:
                        word_list += [idy]
                        if count == 0:
                            new_label[idy.lower()] = 'B-'+label[ori_key]
                            label_list += ['B-'+label[ori_key]]
                        else:
                            new_label[idy.lower()] = 'I-'+label[ori_key]
                            label_list+=['I-'+label[ori_key]]
                        count += 1
                else:
                    for idy in key1:
                        word_list += [idy]
                        new_label[idy.lower()] = 'B-'+label[ori_key]
                        label_list+=['B-'+label[ori_key]]
            
            if idx.lower() in new_label.keys():
                if 'B-' not in new_label[idx.lower()]:
                    if pre_label != 'O':
                        f_write.write(idx+" "+new_label[idx.lower()]+'\n')
                        pre_label = new_label[idx.lower()]
                    elif pre_label == 'O' and 'B-' not in label_list[0]:
                        pass
                    else:
                        if word_list[line_len] != idx:
                            f_write.write(idx + ' ' +'O' +'\n')
                        else:
                            f_write.write(word_list[line_len]+ ' ' + label_list[line_len] +'\n')
                        line_len += 1
                        continue

                elif 'B-' in new_label[idx.lower()]:
                    pre_label = 'B-'
                    f_write.write(idx+" "+new_label[idx.lower()]+'\n')
                    pre_label = new_label[idx.lower()]
                
            elif idx != '\n' and idx != ' ':
                f_write.write(idx+" "+'O'+'\n')
                pre_label = 'O'
        f_write.write('\n')

# data_helper[input_dir, output_dir]
span2bio("new copy.train", "bio.train")
