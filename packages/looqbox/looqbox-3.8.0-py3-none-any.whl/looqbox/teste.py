import looqbox as lq


def looq_response(par):
    return lq.ObjMessage("Testando")

lq.looq_test_question(looq_response, {})

