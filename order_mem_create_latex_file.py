def get_words():
    words = []
    with open('csw21_threes.txt') as f:
        words = f.read().splitlines()
    return words

if __name__ == '__main__':
    words = get_words()
    number_of_words = len(words)
    number_of_columns = 12
    number_of_rows = 62
    current_start_index = 0
    column_format_string = "X" * number_of_columns
    document_content_string = ""
    while current_start_index < number_of_words:
        tabular_contents_string = ""
        for i in range(number_of_rows):
            for j in range(number_of_columns):
                word_index = current_start_index + (number_of_rows * j) + i
                word = "     "
                if word_index < number_of_words:
                    word = words[word_index]
                if j == number_of_columns - 1:
                    tabular_contents_string += "{} \\\\\n".format(word)
                else:			
                    tabular_contents_string += '{} & '.format(word)

        table_string = '''\
\\begin{{table}}[!htbp]
\\begin{{tabularx}}{{\linewidth}}{{{column_format}}}
{tabular_content}\end{{tabularx}}
\end{{table}}'''.format(tabular_content=tabular_contents_string, column_format=column_format_string)

        document_content_string += table_string
        current_start_index += number_of_columns * number_of_rows

    document = '''\
\\documentclass{{article}}

\\usepackage{{tabularx}}
\\usepackage[margin=0.1in,voffset=-0.2in,footskip=0.0in]{{geometry}}
\\usepackage[sfdefault,medium]{{inter}}
\\usepackage[T1]{{fontenc}}

\\begin{{document}}
\\pagestyle{{empty}}
\\noindent
{}
\\end{{document}}'''.format(document_content_string)

    print(document)
