import re
import os
from text_file_clean_up import *

def custom_important_message_recon(string,path):
    list_keywords = string.split()

    clean_text_file(path)

    with open("cleaned_text_file.txt",'r', encoding="utf8") as f:
        messages = f.readlines()
    
    list_imp_messages = []
    for message in messages:
        message = message.strip()
        list_split = message.split(":")
        try:
            if len(list_split)>2:
                for a in range(1,len(list_split)):
                    message_match += list_split[a]
            else:
                message_match = list_split[1]
        except:
            pass

        match = 0
        for keyword in list_keywords:
            if re.search(keyword,message_match,re.I):
                match += 1
        if match>0:
            tup = (message,match)
            list_imp_messages.append(tup)
        else:
            continue
    
    list_imp_messages.sort(key=lambda i:i[1],reverse=True)
    final_return_list = []
    for message,match in list_imp_messages:
        final_return_list.append(message)
    print(final_return_list)
    return final_return_list

path = r"txt_file_upload\WhatsApp Chat with CBS3004_Prof. Nagaraja G.txt"
string = "cat fat lab"
custom_important_message_recon(string,path)