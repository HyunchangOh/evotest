_hcovgen = dict()
def test_me(x, y, z):
    _hcovgen[1] = False
    if y > 13:
        _hcovgen[1] = True
        "1"
        _hcovgen[2] = False
        if x < 2:
            "2"
            z = 3
            _hcovgen[3] = False
            if x < -1:
                _hcovgen[3] = True
                "3"
                z = 1
    else:
        "4"
        x = 2
    y = 50
    _hcovgen[4] = False
    if z == 4:
        _hcovgen[4] = True
        "5"
        z = 1
    else:
        "6"
        _hcovgen[5] = True
        while x < 5:
            _hcovgen[5] = False
            "7"
            x += 1
            z = z + 1
    y = 0

test_me(1,2,3)
print(_hcovgen)