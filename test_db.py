# import mysql.connector
# import threading
# import time

# def simulate_user_request(user_id):
#     try:
#         # MySQL Server se connect karein
#         db = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="Sachit@2005",
#             database="college_db"
#         )
#         cursor = db.cursor()

#         # Fake user entry insert karna (Test ke liye)
#         query = "INSERT INTO users (email, password, name, dob, roll, course, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#         values = (f"test_user_{user_id}@coe.com", "12345", f"StressUser_{user_id}", "2000-01-01", f"R-{user_id}", "BCA", "9999999999")
        
#         cursor.execute(query, values)
#         db.commit()
#         db.close()
#         print(f"User {user_id}: ✅ Success (Data Saved in MySQL)")
#     except Exception as e:
#         print(f"User {user_id}: ❌ Failed - {e}")

# # 100 users ko ek saath (Parallel) simulate karna
# print("Starting Stress Test on MySQL...")
# threads = []
# for i in range(1000):
#     t = threading.Thread(target=simulate_user_request, args=(i,))
#     threads.append(t)
#     t.start()

# for t in threads:
#     t.join()

# print("\n--- Test Finished! Check your Admin Panel or phpMyAdmin ---")


import mysql.connector
import threading
import time

# --- STRESS TEST CONFIGURATION ---
TOTAL_USERS = 1000  # 100 se badha kar 1000 kiya gaya hai
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sachit@2005", # Aapka purana password
    "database": "college_db"
}

def simulate_user_request(user_id):
    """Har thread ek naye user ki database entry simulate karega"""
    try:
        # MySQL Server se connect karein
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        # Fake user entry insert karna
        query = "INSERT INTO users (email, password, name, dob, roll, course, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (
            f"stress_test_{user_id}_{int(time.time())}@coe.com", 
            "password123", 
            f"User_{user_id}", 
            "2000-01-01", 
            f"ST-{user_id}", 
            "BCA", 
            "1234567890"
        )
        
        cursor.execute(query, values)
        db.commit()
        db.close()
        print(f"User {user_id}: ✅ Success (Entry Saved)")
    except Exception as e:
        print(f"User {user_id}: ❌ Failed - {e}")

if __name__ == "__main__":
    print(f"🚀 Starting Enterprise Level Stress Test: {TOTAL_USERS} Concurrent Users...")
    start_time = time.time()
    
    threads = []
    
    # 1000 threads (users) ko parallel chalu karna
    for i in range(TOTAL_USERS):
        t = threading.Thread(target=simulate_user_request, args=(i,))
        threads.append(t)
        t.start()
        
        # Thoda sa gap (Slight delay) taaki OS threads ko handle kar sake
        if i % 100 == 0:
            time.sleep(0.5)

    # Sabhi threads ke khatam hone ka wait karein
    for t in threads:
        t.join()
        
    end_time = time.time()
    print("\n" + "="*40)
    print(f"📊 STRESS TEST COMPLETED")
    print(f"⏱️ Total Time Taken: {round(end_time - start_time, 2)} seconds")
    print(f"📉 Average Request Time: {round((end_time - start_time)/TOTAL_USERS, 4)} seconds")
    print("="*40)