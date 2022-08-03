def format_a_string(self, w_i):
    w_index = w_i
    str_1 = ""
    for i in range(1):
        str_1 = "{:} {:} {:} {:} {:}".format(self.info_list_str[w_index], self.info_list_str[w_index + 1],
                                             self.info_list_str[w_index + 2], self.info_list_str[w_index + 3],
                                             self.info_list_str[w_index + 4])
    return str_1
