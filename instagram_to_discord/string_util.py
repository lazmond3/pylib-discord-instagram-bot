import re


def sophisticate_string(st):
    st_list = st.strip().split("\n")
    new_lst = []
    for ste in st_list:
        ste = ste.strip()
        st = re.sub(r"^.[ \t\n]*$", "", ste)
        new_lst.append(st)
    new_lst = list(filter(lambda x: len(x) != 0, new_lst))
    st = "\n".join(new_lst)
    return re.sub(r"\n\n\n+", "\n\n", st)
