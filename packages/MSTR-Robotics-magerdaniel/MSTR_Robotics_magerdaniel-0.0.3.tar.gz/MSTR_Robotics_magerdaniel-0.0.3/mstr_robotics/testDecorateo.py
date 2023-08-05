def error_handler(funcx):
    def try_func(*args,**kwargs):
        try:
            return funcx(*args,**kwargs)
        except Exception as e:
            print(funcx.__name__)
            if funcx.__name__=='pipi':
                print("HSKAASA")
            if funcx.__name__=='pups':
                print("HSKzzzzzzzz")
            print(e.__str__())

    return try_func

@error_handler
def pipi(t=None,*args,**kwargs):
    print(t + "pipi")

@error_handler
def pups(p,u=None,*args,**kwargs):
    print(p +"pups")
    return
pipi("5")
pups(u="wwwe", p="2",x="WWWWWWW",t="KKKK")

