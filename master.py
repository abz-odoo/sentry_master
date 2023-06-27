from ..slave import slave

def call():
    print("from master")
    print("calling slave from master")
    slave.call()

if __name__ == "__main__":
    call()