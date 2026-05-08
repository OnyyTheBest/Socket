class utils:

    def generate_warning(msg:str) -> None:
        print("[!] {}".format(msg))
    
    def generate_error(msg:str) -> None:
        print("[X] {}".format(msg))
    
    def generate_info(msg:str) -> None:
        print("[|] {}".format(msg))