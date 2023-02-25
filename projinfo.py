class ProjectInfo:
    
    def __init__(self,projname,client="",engfirm="",sitename="",
                 contractor=""):
        self.projname = projname
        self.client = client
        self.engfirm = engfirm
        self.sitename = sitename
        self.contractor = contractor


if __name__=="__main__":

    proj1 = ProjectInfo("ESC Bridge")
    proj1.client = "서울지방국토관리청"
    proj1.contractor = "우리건설"

    print(proj1.projname)
    print(proj1.client)
    print(proj1.engfirm)
    print(proj1.sitename)
    print(proj1.contractor)
