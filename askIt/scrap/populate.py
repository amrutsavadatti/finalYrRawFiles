

# import csv

# # def blah():
# #     with open('askIt/scrap/alumniData.csv', newline='') as f:
# #         reader = csv.reader(f)
# #         data = list(reader)
# #     return data


# with open('/static/alumniData.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = list(reader)

# for j in range(1,len(data)):
#     email = data[j][0]
#     passW = data[j][1]
#     fullName = data[j][2]
#     userName = data[j][3]
#     phone = data[j][4]
#     userT = data[j][5]

#     print( email , passW , fullName)

# #     putData1 = UserCreds(email=email,password=passW)
# #     putData1.save()     


# #     putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phone,userType=userT, keyLink=putData1)
# #     putData.save()

# # start putting in db

# # putData1 = UserCreds(email=email,password=password)
# # putData1.save()
# # pk = UserCreds.objects.filter(email=email)

# # putData = AppUser(fullName=fullName,userName=userName,phoneNumber=phoneNumber,userType=userType, keyLink=putData1)
# # putData.save()