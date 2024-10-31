import random
import mysql.connector as mysql

try:
    conn=mysql.connect(
        host="localhost",
        user="root",
        password="NISHchan@21"
    )

    cur=conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS USER_DATABASE")
    cur.execute("USE USER_DATABASE")
    cur.execute("CREATE TABLE IF NOT EXISTS USER_DATA(USER_NAME VARCHAR(50) PRIMARY KEY, PASSWORD VARCHAR(20) NOT NULL, OTP INT(6), BIOMETRIC VARCHAR(50))")


    # OTP GENERATION FUNCTION

    def generate_otp(user):
        
        otp=str(random.randint(100000,999999))
        try:
            cur.execute("UPDATE USER_DATA SET OTP=%s WHERE USER_NAME=%s",(otp,user))
            conn.commit()
            return otp
        except mysql.Error as e:
            print(f"ERROR:{e}")
            conn.rollback()
            return None

    # BIOMETRIC VERIFICATION FUNCTION

    def verify_biometric(user,biometric_data):
        
        cur.execute("SELECT BIOMETRIC FROM USER_DATA WHERE USER_NAME=%s",(user,))
        result=cur.fetchone()
        
        if result:
            stored_biometric_data=result[0]
            return biometric_data == stored_biometric_data
        else:
            return False
        
    # USER LOGIN FUNCTION

    def login(user,password,auth_method):
        
        cur.execute("SELECT EXISTS(SELECT 1 FROM USER_DATA WHERE USER_NAME =%s)",(user,))
        exists=cur.fetchone()[0]
        
        if not exists:
            return "USER NOT FOUND"
        
        elif auth_method == "password":
            cur.execute("SELECT EXISTS(SELECT 1 FROM USER_DATA WHERE USER_NAME=%s AND PASSWORD=%s)",(user,password,))
            key=cur.fetchone()[0]
            
            if key==1:
                return "LOGIN SUCCESSFULLY WITH PASSWORD"
            else:
                return "INCORRECT PASSWORD"
            
        elif auth_method == "otp":
            cur.execute("SELECT EXISTS(SELECT 1 FROM USER_DATA WHERE USER_NAME=%s AND OTP=%s)",(user,password,))
            key=cur.fetchone()[0]
            
            if key==1:
                return "LOGIN SUCCESSFULLY WITH OTP"
            else:
                return "INCORRECT OTP"
        
        elif auth_method == "biometric":
            
            if verify_biometric(user,password):
                return "LOGIN SUCCESSFULLY WITH BIOMETRIC"
            else:
                return "BIOMETRIC VERIFICATION FAILED"
            
    while True:
        
        name=input("ENTER USERNAME: ")
        print("CHOOSE AUTHENTICATION METHOD:")
        print("1 - PASSWORD")
        print("2 - OTP")
        print("3 - BIOMETRIC")
        print("4 - QUIT")
        choice=input("ENTER THE NUMBER OF YOUR CHOICE(1/2/3/4): ")
        
        if choice=="1":
            passkey=input("ENTER PASSWORD: ")
            res=login(name,passkey,"password")
            break
        
        elif choice=="2":
            otp=generate_otp(name)
            print(f"GENERATED OTP: {otp}")
            passkey=input("ENTER OTP: ")
            res=login(name,passkey,"otp")
            break
        
        elif choice=="3":
            bio=input("ENTER BIOMETRIC DATA: ")
            res=login(name,bio,"biometric")
            break
        
        elif choice=="4":
            print("EXITING PROGRAM")
            break
        
        else:
            print("INVALID CHOICE PLEASE SELECT (1/2/3/4)")

    print(res)

finally:
    if conn.is_connected():
        cur.close()
        conn.close()
        

    
    