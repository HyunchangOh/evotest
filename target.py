hctest={}
def test_me(x, y, z):
    hctest['1.1']=False
    if y > 13:
        hctest['1.1']=True
        "1"
        hctest['1.1.1']=False
        if x < 2:
            hctest['1.1.1']=True
            "2"
            z = 3
            hctest['1.1.1.1']=False
            if x < -1:
                hctest['1.1.1.1']=True
                "3"
                z = 1
    else:
        "4"
        x = 2
    y = 50
    hctest['1.2']=False
    if z == 4:
        hctest['1.2']=True
        "5"
        z = 1
    else:
        "6"
        hctest['1.2.1']=False
        while x < 5:
            hctest['1.2.1']=True
            "7"
            x += 1
            z = z + 1
    y = 0
