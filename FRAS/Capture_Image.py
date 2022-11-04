import csv
import sqlite3
import pyqrcode
import pyzbar.pyzbar as pyzbar
from colorama import Back, Style

import cv2
import os

import os.path
# counting the numbers


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



# Take image function

def database():
	conn = sqlite3.connect('EmployeeDatabase.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS all_record(employee_name TEXT, employee_id TEXT, employee_contact, employee_department TEXT)")
	conn.commit()
	conn.close()


def takeImages():


    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")

    # QR wala code
    Li = []
    E_name=str(name)
    E_id=str(Id)
    Li.extend((E_name,E_id))
    #-----using List Compression to convert a list to str--------------
    listToStr = ' '.join([str(elem) for elem in Li])
    #print(listToStr)
    print("Please Verify the Information")
    print("Employee Name       = "+ E_name)
    print("Employee ID         = "+ E_id)
    input("Press Enter to continue or CTRL+C to Break Operation")
    database()
    conn = sqlite3.connect('EmployeeDatabase.db')
    c = conn.cursor()
    c.execute("INSERT INTO all_record(employee_name, employee_id) VALUES (?,?)", (E_name,E_id))
    conn.commit()
    conn.close()
    qr= pyqrcode.create(listToStr)
    if not os.path.exists('./QrCodes'):
        os.makedirs('./QRCodes')
    qr.png("./QRCodes/" +E_name+ ".png",scale=8)
    print("QRcode Saved in ~QRCodes...")


    # END

    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        while(True):
            ret, img = cam.read()
            if ret == True:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)
                for(x,y,w,h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (10, 159, 255), 2)
                    #incrementing sample number
                    sampleNum = sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage" + os.path.sep +name + "."+Id + '.' +
                                str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                    #display the frame
                cv2.imshow('frame', img)
                #wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 100
                elif sampleNum > 100:
                    break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        print(res)
        header=["Id", "Name"]
        row = [Id, name]
        if(os.path.isfile("StudentDetails"+os.path.sep+"StudentDetails.csv")):
            with open("StudentDetails"+os.path.sep+"StudentDetails.csv", 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(j for j in row)
            csvFile.close()
        else:
            with open("StudentDetails"+os.path.sep+"StudentDetails.csv", 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(i for i in header)
                writer.writerow(j for j in row)
            csvFile.close()
    else:
        if(is_number(Id)):
            print("Enter Alphabetical Name")
        if(name.isalpha()):
            print("Enter Numeric ID")


