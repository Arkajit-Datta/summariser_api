import re
import os

def clean_text_file(path):
    with open(path,'r', encoding="utf8") as f:
        lines = f.readlines()

    new_lines = []
    temp = 0
    for i in lines:
        temp_str = str(i)
        temp_str = temp_str[20:]
        if re.search("joined using this group's invite link",temp_str) or re.search("Messages and calls are end-to-end encrypted",temp_str) or re.search("Media",temp_str) or re.search("created group",temp_str) or re.search("added",temp_str) or re.search("left",temp_str) or re.search("https://",temp_str) or re.search("http://",temp_str) or re.search("This message was deleted",temp_str) :
            pass
        else:
            new_lines.append(temp_str)


    file = open("cleaned_text_file.txt","r+",encoding="utf8")
    file.truncate(0)
    file.close()

    txt_file = open("cleaned_text_file.txt","w",encoding="utf8")
    for elements in new_lines:
        txt_file.write(elements)
    txt_file.close()

# path = r"txt_file_upload\WhatsApp Chat with CBS3004_Prof. Nagaraja G.txt"
# clean_text_file(path)