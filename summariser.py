from transformers import pipeline

summarizer = pipeline("summarization")

def summarise():
    with open("cleaned_text_file.txt",'r', encoding="utf8") as f:
        lines = f.readlines()
    ARTICLE = ""
    # temp_str = lines[5]
    # list_temp = temp_str.split(":")
    # print(list_temp)
    count = 0
    for i in lines:
        temp_str = str(i)
        list_temp = temp_str.split(":")

        if len(list_temp)==2:
            try:
                temp_str_1 = list_temp[1]
                temp_str_1 = temp_str_1[0:-1]
                ARTICLE += temp_str_1
                count += 1
            except:
                pass
            
    #print(ARTICLE)
    list_summary = summarizer(ARTICLE, max_length=200, min_length=10, do_sample=False, truncation=True)
    #print(list_summary[0])
    return list_summary[0]
#summarise()