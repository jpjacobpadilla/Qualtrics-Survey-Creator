from queue import Queue


def mod_ten_conversation_id_list(survey_index):
  _cid = Queue()

  if survey_index != 10:
    num = survey_index
  else:
      num = 0

  for index in range(1, 501):
    if index % 10 == num:
        _cid.put(index)
  
  return _cid