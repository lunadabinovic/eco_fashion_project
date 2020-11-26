import re
import string

def get_pct(ind_df, fb_key):
    int_tag_lines = ind_df.loc[fb_key][1]
    pt = re.search(r'((\d+)[%])',int_tag_lines[0])
    if pt:
        pct = pt.group(0)
    else:
        pct = '%'

    return pct


def percentages_to_float(df):
    percentage_final_list = []

    if df is not None:
        tag_score_df = df.set_index('fiber')
        pct_list = tag_score_df['percentage'].tolist()

        punctuations = string.punctuation
        clean_strings = [''.join(x for x in string if x not in punctuations) for string in pct_list]

        if clean_strings:
            for number in clean_strings:
                if number:
                    final_number = float(number)/100
                else:
                    final_number = 0
                percentage_final_list.append(final_number)
        # else clean_strings = list with all 0?

    return percentage_final_list


def check_100_pct(percentage_list):
    if sum(percentage_list) != 1.0:
        return ":exclamation: Please check the composition of the label: percentages do not add up to 100%"
    #pass
    return ":white_check_mark: Checked: the percentages add up to 100%"

def get_score(fiber_score_df, df):
    score_list = []
    tag_score_df = df.set_index('fiber')

    for fiber_id, row in tag_score_df.iterrows():
        score_list.append(fiber_score_df.loc[f"{fiber_id}"]['Final Score'])

    return score_list

def convert_5scale_to_emoji(score):
    if score > 4.0 and score <= 5.0:
        return ":smiley:"
    elif score > 3.0 and score <= 4.0:
        return ":smile:"
    elif score > 2.0 and score <= 3.0:
        return ":neutral_face:"
    elif score > 1.0 and score <= 2.0:
        return ":cry:"
    elif score > 0.0 and score <= 1.0:
        return ":sob:"

def convert_pct_to_emoji(pct):
    if pct > 0.8 and pct <= 1.0:
        return ":smiley:"
    elif pct > 0.6 and pct <= 0.8:
        return ":smile:"
    elif pct > 0.4 and pct <= 0.6:
        return ":neutral_face:"
    elif pct > 0.2 and pct <= 0.4:
        return ":cry:"
    elif pct > 0.0 and pct <= 0.2:
        return ":sob:"
