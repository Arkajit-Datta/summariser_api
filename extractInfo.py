from operator import itemgetter
import unicodedata
import re

# file=fitz.open(r'email_test_cases\test_02.pdf')


class ExtractLiterature:
    def __init__(self,file) -> None:
        self.file = file
    def fonts(self,doc, granularity=False):
        """
        Extracts fonts and their usage in PDF documents.
        :param doc: PDF document to iterate through
        :type doc: <class 'fitz.fitz.Document'>
        :param granularity: also use 'font', 'flags' and 'color' to discriminate text
        :type granularity: bool
        :rtype: [(font_size, count), (font_size, count}], dict
        :return: most used fonts sorted by count, font style information
        """
        styles = {}
        font_counts = {}

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:  # iterate through the text blocks
                if b['type'] == 0:  # block contains text
                    for l in b["lines"]:  # iterate through the text lines
                        for s in l["spans"]:  # iterate through the text spans
                            print("lines detected --> {}".format(s['text']))
                            if granularity:
                                identifier = "{0}{1}{2}_{3}".format(s['size'], s['flags'], s['font'], s['color'])
                                styles[identifier] = {'size': s['size'], 'flags': s['flags'], 'font': s['font'],
                                                    'color': s['color']}
                            else:
                                identifier = "{0}".format(s['size'])
                                styles[identifier] = {'size': s['size'], 'font': s['font']}

                            font_counts[identifier] = font_counts.get(identifier, 0) + 1  # count the fonts usage
                print("Next Block...")

        font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

        if len(font_counts) < 1:
            raise ValueError("Zero discriminating fonts found!")

        return font_counts, styles

    def font_tags(self,font_counts, styles):
        """Returns dictionary with font sizes as keys and tags as value.
        :param font_counts: (font_size, count) for all fonts occuring in document
        :type font_counts: list
        :param styles: all styles found in the document
        :type styles: dict
        :rtype: dict
        :return: all element tags based on font-sizes
        """
        p_style = styles[font_counts[0][0]]  # get style for most used font by count (paragraph)
        p_size = p_style['size']  # get the paragraph's size

        # sorting the font sizes high to low, so that we can append the right integer to each tag 
        font_sizes = []
        for (font_size, count) in font_counts:
            f_size = styles[font_size]['size']
            font_sizes.append(float(f_size))
        font_sizes.sort(reverse=True)

        # aggregating the tags for each font size
        idx = 0
        size_tag = {}
        for size in font_sizes:
            idx += 1
            if size == p_size:
                idx = 0
                size_tag[size] = '<p>'
            if size > p_size:
                size_tag[size] = '<h{0}>'.format(idx)
            elif size < p_size:
                size_tag[size] = '<s{0}>'.format(idx)

        return size_tag
    def headers_para(self, doc, size_tag):
        """Scrapes headers & paragraphs from PDF and return texts with element tags.
        :param doc: PDF document to iterate through
        :type doc: <class 'fitz.fitz.Document'>
        :param size_tag: textual element tags for each size
        :type size_tag: dict
        :rtype: list
        :return: texts with pre-prended element tags
        """
        header_para = []  # list with headers and paragraphs
        first = True  # boolean operator for first header
        previous_s = {}  # previous span

        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            for b in blocks:  # iterate through the text blocks
                if b['type'] == 0:  # this block contains text
                    # REMEMBER: multiple fonts and sizes are possible IN one block
                    block_string = ""  # text found in block
                    for l in b["lines"]:  # iterate through the text lines
                        for s in l["spans"]:  # iterate through the text spans
                            if s['text'].strip():  # removing whitespaces:
                                if first:
                                    previous_s = s
                                    first = False
                                    block_string = size_tag[s['size']] + s['text']
                                else:
                                    if s['size'] == previous_s['size']:

                                        if block_string and all((c == "|") for c in block_string):
                                            # block_string only contains pipes
                                            block_string = size_tag[s['size']] + s['text']
                                        if block_string == "":
                                            # new block has started, so append size tag
                                            block_string = size_tag[s['size']] + s['text']
                                        else:  # in the same block, so concatenate strings
                                            block_string += " " + s['text']

                                    else:
                                        clean_text = unicodedata.normalize("NFKD", block_string)
                                        header_para.append(clean_text)
                                        block_string = size_tag[s['size']] + s['text']

                                    previous_s = s

                        # new block started, indicating with a pipe
                        block_string += "|"
                    clean_text = unicodedata.normalize("NFKD", block_string)
                    header_para.append(clean_text)

        return header_para
    #calling this single method to extract the information from the PDF file
    def extract(self):
        font_count, style = self.fonts(self.file)
        font_tags_list = self.font_tags(font_counts=font_count,styles=style)
        return self.headers_para(self.file, font_tags_list)

    #This Method will extract the paragraphs from the 
    def extract_paragraphs(self):
        final_para = ""
        extracted_info = self.extract()
        header_reg = re.compile(r"<(p|s|h)[1-9]?>")
        for para in extracted_info:
            header = header_reg.match(para)
            if header is not None:
                if header[0] == "<p>": #then its a paragraph
                    para = re.sub(r"<p>","",para)
                    new_para = re.sub(r"[\|]","",para)
                    final_para += new_para
        return final_para
# extract_obj = ExtractLiterature(file=file)
# print(extract_obj.extract_paragraphs())