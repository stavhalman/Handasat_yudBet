picturePath = 'itaygaming.png'
with open (picturePath,'rb') as file:
    data=file.read()
print(len(data)/1024)
