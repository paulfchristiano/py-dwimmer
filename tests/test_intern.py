from intern import *
import pytest

def debug():
    import ipdb
    ipdb.set_trace()

@pytest.mark.parametrize("encoder,decoder,inputs",[
    (intern_string, get_string, ["hi", "hello", "test", "hello", "test", "this"]),
    (intern_int, get_int, [3, 4, 1004792, 0, 3, 1004792, 3]),
    (intern_pair, get_pair, [(3, 4), (2, 5), (3, 4)]),
    (intern_list, get_list, [[3, 4, 5], [3, 4, 5], [3, 4], [], [], [3], [4], [4], [3, 4, 6]])
])
def test_interning(encoder, decoder, inputs):
    ids = [encoder(s) for s in inputs]
    for s, id in zip(inputs, ids):
        assert decoder(id) == s
        for s2, id2 in zip(inputs, ids):
            if s == s2:
                assert id == id2

@pytest.mark.parametrize("start,last,out", [
    ([1, 2, 3], 4, [1, 2, 3, 4]),
    ([], 4, [4]),
    ([-1], -1, [-1, -1])
])
def test_exending(start, last, out):
    id = intern_list(start)
    id = extend_list(id, last)
    assert out == get_list(id)

@pytest.mark.parametrize("var, template", [
    (3, 0),
    ("hello", ""),
    ((2, 4), (0, 0)),
    ([1, 2, 3], [0]),
    (("hello", [(3, "hi")]), ("", [(0, "")]))
])
def test_general(var, template):
    id = intern_all(var)
    assert var == get_all(id, template)
