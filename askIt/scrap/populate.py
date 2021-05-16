
# import csv

# # # def blah():
# # #     with open('askIt/scrap/alumniData.csv', newline='') as f:
# # #         reader = csv.reader(f)
# # #         data = list(reader)
# # #     return data


# # with open('/static/alumniData.csv', newline='') as f:
# #     reader = csv.reader(f)
# #     data = list(reader)

# # for j in range(1,len(data)):
# #     email = data[j][0]
# #     passW = data[j][1]
# #     fullName = data[j][2]
# #     userName = data[j][3]
# #     phone = data[j][4]
# #     userT = data[j][5]

# #     print( email , passW , fullName)

# # #     putData1 = UserCreds(email=email,password=passW)
# # #     putData1.save()     


# # #     putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phone,userType=userT, keyLink=putData1)
# # #     putData.save()

# # # start putting in db

# # # putData1 = UserCreds(email=email,password=password)
# # # putData1.save()
# # # pk = UserCreds.objects.filter(email=email)

# # # putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phoneNumber,userType=userType, keyLink=putData1)
# # # putData.save()

# with open('C:/Users/Amrut/Desktop/askIt/finalYrRawFiles/askIt/scrap/QnA.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)

# for j in range(1,len(data)):
#     print("Question")
#     qstn = data[j][0]
#     print(qstn)
#     for i in range(1,3):
#         print(data[j][i])

#     print("#################")

# with open('C:/Users/Amrut/Desktop/askIt2021/finalYrRawFiles/askIt/scrap/comments2.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)

# for j in range(2,len(data)):
#     print("Ans")
#     ans = data[j][0]
#     cTo = data[j][3]
#     pos = data[j][4]
#     auth = data[j][5]
#     reply = data[j][6]
#     if reply:
#         print("REPLYYY")
#         print(ans,cTo,pos,auth,reply)
#         continue
#     print(ans,cTo,pos,auth)
    

#     print("#################")
