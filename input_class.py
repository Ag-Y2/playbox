class Userdata:
    def __init__(self):
        self.username = "hi username"
        self.pw = ""
        self.comm = ""
        self.file_path = ""

    def set_username(self, name):
        self.username = name

    def set_pw(self, password):
        self.pw = password

    def set_comm(self, commend):
        self.comm = commend

    def set_filepath(self, path):
        print('----in set filepath, path is', path)
        self.file_path = path

    ############------getter------#########

    def get_username(self):
        return self.username
    
    def get_pw(self):
        return self.pw
    
    def get_comm(self):
        return self.comm
    
    def get_filepath(self):
        return self.file_path