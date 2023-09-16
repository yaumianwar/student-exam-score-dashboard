def get_total_page(page_size, total_data):
  data_div_page_size = total_data // page_size
  data_mod_page_size = total_data % page_size
  total_page = data_div_page_size if data_mod_page_size == 0 else (data_div_page_size+1)

  return total_page 