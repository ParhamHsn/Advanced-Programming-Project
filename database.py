class table:
    def __init__(self,name):
        self.name = name
        self.f = []
class feature(table):
    def __init__(self,name,unique,ftype):
        self.name = name
        self.unique = unique
        self.ftype = ftype
file = open("schema.txt", "r")
count = 0
tb = []
while True:
    count += 1
    line = file.readline()
    if not line:
        break
    s = line.strip()
    if s == "":
        continue
    #print(s)
    if(len(s.split()) == 1):
        if(count!=1):
            tb.append(t)
        t = table(s)
    else:
        if(len(s.split()) == 2):
            s = s.split()
            f = feature(s[0],"no",s[1])
            t.f.append(f)
        else:
            s = s.split()
            f = feature(s[0], "yes",s[2])
            t.f.append(f)
tb.append(t)
file.close()
#print(tb[1].f[1].ftype)






import os.path

for i in range(len(tb)):
    file_name = str(tb[i].name+".txt")
    #print(file_name)
    if os.path.isfile(file_name):
        pass
    else:
        file = open(file_name, 'w')
        string = "id "
        for j in range(len(tb[i].f)):
            string += str(tb[i].f[j].name+" ")
        file.write(string)
        file.close()

class sql:
    def __init__(self, query):
        self.query = query
        self.error = 0
        if self.query[len(self.query)-1] != ";":
            self.error = 1
        if self.query[0] != "$":
            self.error = 4
    def ERROR(self):
        if self.error == 1:
            print("ERROR : Semicolon At The End Of Your Query !")
        if self.error == 2:
            print("ERROR : The Length Of Value For " + self.value + " Is Not In The Range !")
        if self.error == 3:
            print("ERROR : The Value For " + self.value + " Is Not Unique !")
        if self.error == 4:
            print("ERROR : $ At The Beginning Of Your Query !")
        if self.error == 5:
            print("ERROR : Query Must Be Uppercase !")
    def insert(self):
        val = self.query.split()[len(self.query.split())-1]
        val = val[1:len(val)-2]
        val = val.split(",")
        file_name = self.query.split()[3]
        #CHECK
        for i in range(len(tb)):
            if tb[i].name == file_name:
                for j in range(len(tb[i].f)):
                    if tb[i].f[j].ftype[0:4] == "CHAR":
                        maximum = int(tb[i].f[j].ftype[5:len(tb[i].f[j].ftype)-1])
                        if len(val[j]) > maximum:
                            self.error = 2
                            self.value = tb[i].f[j].name
                    if tb[i].f[j].unique == "yes":
                        file = open(str(tb[i].name+".txt"), "r")
                        count = 0
                        while True:
                            count += 1
                            line = file.readline()
                            if not line:
                                break
                            s = line.strip()
                            if count > 1:
                                s = s.split()[j+1]
                                if s == val[j]:
                                    self.error = 3
                                    self.value = tb[i].f[j].name
                        file.close()
        if(self.error == 0): 
            file_name += ".txt"
            file = open(file_name, "r")
            count = len(file.readlines())
            file.close()
            file = open(file_name, 'r')
            cnt = 0
            while True:
                cnt += 1
                line = file.readline()
                if not line:
                    break
                s = line.strip().split()
                if count == cnt:
                    if cnt == 1:
                        last_id = "0"
                    else:
                        last_id = s[0] 
            file.close()
            file = open(file_name, 'a')
            string = "\n"
            string += str(int(last_id)+1) + " "
            for i in val:
                string += i + " "
            file.write(string)
            file.close()
        else:
            self.ERROR()
    def select(self):
        l = []
        self.query = self.query[:len(self.query)-1]
        val = self.query.split()
        for i in range(len(val)):
            if val[i] == "WHERE":
                file_name = val[i-1]
                indx = sql.check(val[i-1]," ".join(val[i+1:len(val)]))
                break 
        if self.error == 0:    
            file = open(file_name + ".txt", 'r')
            count = 0
            while True:
                line = file.readline()
                if not line:
                    break
                s = line.strip()
                if count == 0:
                    #print(s)      #### FIRST ROW IN DATABASE
                    l.append(s)
                else:
                    if int(s.split()[0]) in indx:
                        #print(s)       #### DATA
                        l.append(s)
                count += 1
            file.close()
            return(l)
        else:
            self.ERROR()
    def delete(self):
        self.query = self.query[:len(self.query)-1]
        val = self.query.split()
        for i in range(len(val)):
            if val[i] == "WHERE":
                file_name = val[i-1]
                indx = sql.check(val[i-1]," ".join(val[i+1:len(val)]))
                break 
        if self.error == 0:
            string = ""
            file = open(file_name + ".txt", 'r')
            count = 0
            while True:
                line = file.readline()
                if not line:
                    break
                s = line.strip()
                if count == 0:
                    string += s
                elif int(s.split()[0]) in indx:
                    continue
                else:
                    string += s
                count += 1
                string += "\n"
            file.close()
            string = string.strip()
            #print(string)
            file = open(file_name + ".txt", 'w')
            file.write(string)
            file.close()
        else:
            self.ERROR()
    def update(self):
        val = self.query.split()
        start = 0
        end = 0
        for i in range(len(val)):
            if val[i] == "WHERE":
                file_name = val[i-1]
                start = i + 1
            elif val[i] == "VALUES":
                end = i
        indx = sql.check(file_name," ".join(val[start:end]))
        #print(indx)
        val = self.query.split()[len(self.query.split())-1]
        val = val[1:len(val)-2]
        val = val.split(",")
        # #CHECK
        # for i in range(len(tb)):
        #     if tb[i].name == file_name:
        #         for j in range(len(tb[i].f)):
        #             if tb[i].f[j].ftype[0:4] == "CHAR":
        #                 maximum = int(tb[i].f[j].ftype[5:len(tb[i].f[j].ftype)-1])
        #                 if len(val[j]) > maximum:
        #                     self.error = 2
        #             if tb[i].f[j].unique == "yes":
        #                 file = open(str(tb[i].name+".txt"), "r")
        #                 count = 0
        #                 while True:
        #                     count += 1
        #                     line = file.readline()
        #                     if not line:
        #                         break
        #                     s = line.strip()
        #                     if count > 1:
        #                         s = s.split()[j+1]
        #                         if s == val[j]:
        #                             self.error = 3
        #                 file.close()
        if self.error == 0: 
            string = ""
            file = open(file_name + ".txt", 'r')
            count = 0
            new_values = " ".join(val)
            while True:
                line = file.readline()
                if not line:
                    break
                s = line.strip()
                if count == 0:
                    string += s
                elif int(s.split()[0]) in indx:
                    string += str(count) + " " + new_values
                else:
                    string += s
                count += 1
                string += "\n"
            file.close()
            string = string.strip()
            #print(string)
            file = open(file_name + ".txt", 'w')
            file.write(string)
            file.close()
        else:
            self.ERROR()
    def one_check(table_name ,x):
        #print(x.split())
        indx = set()
        left = x.split()[0]
        right = x.split()[2][1:len(x.split()[2])-1]
        mid = x.split()[1]
        file = open(table_name + ".txt", 'r')
        count = 0
        j = 0
        while True:
            count += 1
            line = file.readline()
            if not line:
                break
            s = line.strip().split()
            if count == 1:
                for i in range(len(s)):
                    if(left == s[i]):
                        j = i
                        break
            else:
                if mid == "==":
                    if s[j] == right:
                        indx.add(int(s[0]))
                else:
                    if s[j] != right:
                        indx.add(int(s[0]))
        file.close()
        return(indx)
    def check(table_name , x):
        lst = []
        AndOr = []
        s = x.split()
        if len(s) == 3:
            return(sql.one_check(table_name,x))
        else:
            first = 0
            for i in range(0,len(s)):
                if s[i] == "AND" or s[i] == "OR" or i == len(s) - 1:
                    if i != len(s) - 1:
                        lst.append(sql.one_check(table_name," ".join(s[first:i])))
                    else:
                        lst.append(sql.one_check(table_name," ".join(s[first:])))
                    if s[i] == "AND" or s[i] == "OR":
                        AndOr.append(s[i])
                    first = i + 1
            final = set()
            for i in range(len(AndOr)):
                if i == 0:
                    if AndOr[i] == "AND":
                        final = lst[i].intersection(lst[i+1])
                    else:
                        final = lst[i].union(lst[i+1])
                else:
                    if AndOr[i] == "AND":
                        final = final.intersection(lst[i+1])
                    else:
                        final = final.union(lst[i+1])
            return(final)
    def mainCheck(self):
        if self.query.split()[1] == "INSERT":
            self.insert()
        elif self.query.split()[1] == "SELECT":
            return(self.select())
        elif self.query.split()[1] == "DELETE":
            self.delete()
        elif self.query.split()[1] == "UPDATE":
            self.update()
        else:
            self.error = 5
# q1 = "$ INSERT INTO User VALUES (parham,123456,1594823426.159446);"
# s1 = sql(q1)
# s1.insert()
# q2 = "$ INSERT INTO User VALUES (nima,654321,1594823426.159446);"
# s2 = sql(q2)
# s2.insert()
# q3 = "$ INSERT INTO User VALUES (nima,asda564,1594823426.159446);"
# s3 = sql(q3)
# s3.insert()
# q3 = "$ INSERT INTO User VALUES (asghar,1222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222297,1594823426.159446);"
# s3 = sql(q3)
# s3.insert()
#sql.check("((User = 'eminem' OR Phone = '09386208211') OR (gender = male OR Age = 23)) OR (password = 123)")
#sql.check("user","username == 'eminem' OR phone == '09386208211 OR gender == male'")
#print(sql.check("User","username == 'parham' OR password == '65432' OR joined_at == '1594823426.159446'"))
#print(sql.check("User","password == '654321'"))
#print(sql.check("User","password == '654321'"))
# q4 = "$ SELECT FROM User WHERE username == 'arham' OR password == '654321';"
# s4 = sql(q4)
# s4.select()
# q5 = "$ DELETE FROM User WHERE password == '123456' AND username == 'nima';"
# s5 = sql(q5)
# s5.delete()
# q6 = "$ UPDATE User WHERE password == '123456' AND username == 'parham' VALUES (parham,AsFg45623,1594823426.159446);"
# s6 = sql(q6)
# s6.update()
# q1 = "$ INSERT INTO User VALUES (ahmad,23asdg_asW456,1594823426.159446);"
# s1 = sql(q1)
# s1.mainCheck()
#print(sql.check("BankAcounts","alias == 'par'"))
#query = input("")
#s = sql(query)
#s.mainCheck()