import os
from dotenv import load_dotenv
import mysql.connector
# import mysql
load_dotenv()

def update_database_safely():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        
        # db = mysql.connector.connect(
        #       host=os.getenv("DB_HOST"),
        #       user=os.getenv("DB_USER"),
        #       password=os.getenv("DB_PASSWORD"),
        #       port=os.getenv("DB_PORT"),
        #       database="college_db",
        #       ssl_ca="ca.pem",      
        #       ssl_verify_cert=True
        # )

        cursor = db.cursor(buffered=True) 

        # 2. Database create 
        cursor.execute("CREATE DATABASE IF NOT EXISTS college_db")
        cursor.execute("USE college_db")

        # 3. Tables Creation (IF NOT EXISTS ensures no data loss)
        
        # Users Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY, 
            password VARCHAR(255) NOT NULL, 
            name VARCHAR(255) NOT NULL, 
            dob VARCHAR(50), 
            gender VARCHAR(20), 
            roll VARCHAR(50), 
            course VARCHAR(100), 
            phone VARCHAR(20),
            attendance VARCHAR(50) DEFAULT '0',       
            internal_grade VARCHAR(20) DEFAULT 'N/A'             
        )''')

        # Results Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255),
            subject VARCHAR(255) NOT NULL,
            marks INT NOT NULL,
            total_marks INT DEFAULT 100,
            semester VARCHAR(50),
            FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
        )''')

        # ID Card Applications Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS id_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            full_name VARCHAR(255) NOT NULL,
            gender VARCHAR(20),
            father_name VARCHAR(255),
            mother_name VARCHAR(255),
            roll_no VARCHAR(50) NOT NULL,
            department VARCHAR(100),
            academic_year VARCHAR(50),
            phone VARCHAR(20),
            photo_path VARCHAR(255),
            signature_path VARCHAR(255),
            marksheet_path VARCHAR(255),
            status VARCHAR(20) DEFAULT 'Pending',
            unique_id VARCHAR(50) DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
        )''')

        # College Information Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS college_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(100), 
            content LONGTEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Timetable Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS timetable (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course VARCHAR(50), 
            year_sem VARCHAR(50), 
            time_slot VARCHAR(100), 
            subject VARCHAR(255), 
            room_no VARCHAR(100)
        )''')

        # Chat History Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            user_email VARCHAR(255), 
            user_query TEXT, 
            bot_response TEXT, 
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Import History Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS import_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            total_records INT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            admin_email VARCHAR(255) DEFAULT 'admin@coe.control'
        )''')


# Study Material Table (Notes Hub )
        cursor.execute('''CREATE TABLE IF NOT EXISTS study_notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject VARCHAR(100) NOT NULL,
            title VARCHAR(255) NOT NULL,
            file_path VARCHAR(255) NOT NULL,
            uploaded_by VARCHAR(100) DEFAULT 'Admin',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
      
# Community Chat Table 
        cursor.execute('''CREATE TABLE IF NOT EXISTS community_chats (
          id INT AUTO_INCREMENT PRIMARY KEY,
           user_email VARCHAR(255),
           user_name VARCHAR(255),
            message TEXT NOT NULL,
           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
           FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE
         )''')

        # DYNAMIC DATA INSERTION  
        college_data = [
            ('Institutional Name', 'Centre of Excellence, Government College Sanjauli, Shimla.'),
            ('Address', 'Sanjauli, Shimla, Himachal Pradesh, PIN - 171006.'),
            ('Contact Details', 'Phone: 0177-2640332 | Email: principalsanjauli@gmail.com.'),
            ('Official Website', 'www.gcsanjauli.edu.in.'),
            ('NAAC Accreditation', 'The college is accredited with an A+ Grade by NAAC (2023 Cycle).'),
            ('History', 'Established in 1869 as a school and converted into a degree college in 1969.'),
            ('Academic Programs', 'Offers Undergraduate courses in Arts (BA), Science (BSc), Commerce (BCom), Computer Applications (BCA), and Vocational studies (B.Voc).'),
            ('Campus Facilities', 'Equipped with a digitized library, modern science labs, IT labs, a multipurpose hall, and sports facilities.'),
            ('Student Strength', 'Over 3000+ students are currently enrolled across various disciplines.'),
            ('Scholarships', 'Provides various state and central government scholarships including Post-Matric and Merit-based schemes.'),
            ('Faculty', 'Staffed by over 50+ highly qualified professors and academic experts.'),
            ('Vision', 'To provide quality education that empowers students with knowledge and character.'),
            ('Mission', 'To foster an environment of learning and innovation that prepares students for global challenges.'),
            ('Location Info', 'Situated approximately 12 KM from the ISBT Shimla and easily accessible via local transport.'),
            ('English Faculty', 'Dr. Deepak Keprate, Dr. Himani Saxena, Dr. Shiwani Khatri, Dr. Harsh Vardhan Singh Khimta, Dr. Pooja Dulta, Dr. Aditya Singh Dulta, Ms. Anupama Chaudhary, Mr. Vishal Rangta (On Study Leave), Dr. Harsh Bhardwaj.'),
            ('Hindi Faculty', 'Dr. Dinesh Kumari, Mr. Sat Pal, Mr. Arun Kumar.'),
            ('History Faculty', 'Mr. Vikram Bhardwaj, Dr. Chander Verma.'),
            ('Economics Faculty', 'Dr. Madan Shandil, Mrs. Kreety Thakur.'),
            ('Political Science Faculty', 'Dr. Poonam Chandel.'),
            ('Geography Faculty', 'Dr. Bachan Singh, Mrs. Mona Sharma.'),
            ('Sanskrit Faculty', 'Dr. Rakesh Sharma.'),
            ('Sociology Faculty', 'Mr. Prashant Thakur, Dr. Ravinder Kumar.'),
            ('Philosophy Faculty', 'Dr. Poonama Verma.'),
            ('Journalism & Mass Communication Faculty', 'Sh. Sandesh Kumar Kalta.'),
            ('Physical Education Faculty', 'Dr. Satish.'),
            ('Public Administration Faculty', 'Dr. Saroj Devi, Dr. Purnima Thapar.'),
            ('Psychology Faculty', 'Mr. Akshay Azad.'),
            ('Music Faculty', 'Dr. Vinod Kumar, Dr. O.P. Kaul.'),
            ('Botany Faculty', 'Mrs. Deepti Gupta, Dr. Sushil Sharma, Dr. Shikha Chandel.'),
            ('Zoology Faculty', 'Dr. Minakshi Sharma, Dr. Shweta Sharma, Ms. Sarla Thakur.'),
            ('Physics Faculty', 'Dr. Kirti Singha, Sh. Narender Singh.'),
            ('Chemistry Faculty', 'Mrs. Shalu Chauhan, Mrs. Rita Chandel, Dr. Yogesh Kumar.'),
            ('Computer Science Faculty', 'Sh. Surinder Chauhan.'),
            ('Mathematics Faculty', 'Dr. Girish Kapoor, Dr. Anjana Sharma, Dr. Poonam Sharma.'),
            ('Environmental Science Faculty', 'Dr. Lakhbeer Singh.'),
            ('Geology Faculty', 'Dr. Laxmi Versain.'),
            ('Commerce Faculty', 'Dr. Rajender Singh, Dr. Anupam Verma, Dr. Reena Thakur.'),
            ('BCA/PGDCA Faculty', 'Mr. Muneet Lakhanpal (Guest Faculty), Mrs. Pratiksha Chauhan (Guest Faculty), Mrs. Priyanka Chauhan (Guest Faculty), Mrs. Sheetal Chauhan (Guest Faculty), Mr. Ashok Kumar (Guest Faculty).'),
            ('BCA/PGDCA Support Staff', 'Mr. Sanjeev Meghta (System Analyst), Mr. Praveen Jogta (Clerk), Mr. Rohit Verma (Lab. Assistant), Mr. Abhishek Thakur (Peon).'),
            ('BBA Faculty', 'Mrs. Anita Verma (Guest Faculty), Miss. Shweta Thakur (Guest Faculty), Miss. Sakshi (Guest Faculty), Dr. Razal Panta (Guest Faculty), Miss. Komal Sharma (Guest Faculty).'),
            ('BBA Support Staff', 'Office Assistant (Vacant), Mrs. Sangita (Helper).'),
            ('B.Voc Faculty', 'Mr. Pankaj Verma (Vocational Trainer), Mrs. Uma Kanwar (Vocational Trainer), Mr. Suraj Jamalta (Vocational Trainer), Mrs. Surbhi Sharma (Vocational Trainer), Mr. Umesh Rana (Vocational Trainer), Mrs. Pinky (Vocational Trainer).'),
            ('B.Voc Support Staff', 'Mr. Sanjeev Sharma (MIS), Miss. Minakshi Sharma (Lab. Attendant), Mrs. Anuradha Dhiman (Lab. Attendant).'),
           #principal faculty
            ('Previous Principal - Smt. Bharti Bhagra', 'Served from 21.08.2023 to present.'),
            ('Previous Principal - Dr. Bhupinder Singh Thakur (Offg)', 'Served from 08.04.2023 to 21.08.2023.'),
            ('Previous Principal - Dr. C.B. Mehta', 'Served from 12.07.2018 to 31.03.2023.'),
            ('Previous Principal - Smt. Diksha Malhotra', 'Served from 11.04.2016 to 10.07.2018.'),
            ('Previous Principal - Smt. Navendu Sharma (Offg)', 'Served from 01.04.2016 to 11.04.2016.'),
            ('Previous Principal - Dr. Joginder Singh Negi', 'Served from 09.01.2015 to 31.03.2016.'),
            ('Previous Principal - Dr. Uma Pandey', 'Served from 01.05.2012 to 08.01.2015.'),
            ('Previous Principal - Dr. Karuna Bhardwaj (Offg)', 'Served from 09.04.2012 to 31.04.2012.'),
            ('Previous Principal - Dr. Amar Dev', 'Served from 09.04.2008 to 09.04.2012.'),
            ('Previous Principal - Dr. R.L. Vesta', 'Served from 10.04.2005 to 09.04.2008.'),
            ('Previous Principal - Dr. Amar Dev', 'Served from 14.05.2001 to 30.06.2005.'),
            ('Previous Principal - Dr. B.R. Gupta (Offg)', 'Served from 15.02.2001 to 15.05.2001.'),
            ('Previous Principal - Dr. O.P. Gupta (Offg)', 'Served from 16.01.2001 to 14.02.2001.'),
            ('Previous Principal - Dr. S.K. Bhalaik', 'Served from 01.09.1997 to 02.01.2001.'),
            ('Previous Principal - Dr. Anita Rao', 'Served from 01.05.1996 to 31.08.1997.'),
            ('Previous Principal - Dr. S.L. Bhatnagar', 'Served from 09.04.1993 to 31.04.1996.'),
            ('Previous Principal - Mrs. Satish Verma (Offg)', 'Served from 01.04.1993 to 03.04.1993.'),
            ('Previous Principal - Sh. M. Raheja', 'Served from 03.12.1988 to 30.03.1993.'),
            ('Administrative Staff', 'Mr. Sanjeev Kumar Chauhan (Supdt. G-I-cum-DDO), Mr. Anil Kumar (Superintendent G-II), Mr. Nand Lal Verma (Sr. Asst.).'),
            ('IT & Clerical Staff (JOA IT)', 'Mrs. Vidushi, Mr. Mukul Jistu, Miss. Anchal Sharma, Mr. Ajay Kumar.'),
            ('Support Staff (Peon)', 'Mr. Raj Kumar, Mr. Parkashvati, Mrs. Kanta Devi, Mrs. Dolma, Mr. Suresh Kumar, Mrs. Leelavati, Mrs. Ambika, Mrs. Kanta Devi, Mr. Ashok Kumar, Mrs. Babbu Devi, Mrs. Santoshi Devi, Mrs. Priya Dutta.'),
            ('Laboratory Staff - SLA', 'Mr. Hem Chand Sharma (SLA), Mr. Mangat Ram Dhanta (SLA), Mr. Rajinder Singh (SLA).'),
            ('Laboratory Staff - LA', 'Mrs. Sunita Thakur (LA), Mrs. Somba Devi, Parmod Kumar (LA), Mr. Lajpat Rai (LA), Mr. Gulab Singh (LA), Mr. Virinder Singh Thakur (LA), Mrs. Meena Sharma (LA), Mrs. Giano Devi (LA), Mr. Dev Dutt (LA), Mr. Pyare Lal (LA), Mr. Tek Chand (LA).'),
    

            # Admission and Login Instructions
       
            ('Admission Process', 'Applicants must apply online through the official website: https://admissions.gcsanjauli.edu.in. No other mode of application is accepted.'),
            ('Online Application Steps', '1. Register with a valid Email ID and Mobile Number. 2. Verify email before logging in. 3. Fill out the application form carefully and click SAVE. 4. Upload required documents in the provided links. 5. Size of documents should not exceed 1 MB.'),
            ('Required Documents for Admission', 'Candidates need to upload: 1. Matriculation/DOB Certificate. 2. Graduation Certificate (if applicable). 3. Character Certificate. 4. Supporting documents for reservation, fees relaxation, etc. 5. Recent passport size photograph (not exceeding 50 KB, 4.5 X 3.5 cm).'),
            ('Fees Payment Instructions', 'Fees must be paid online. After submitting the application, click on the "Pay prospectus fee" link on the dashboard. Applications without fee payment will not be accepted.'),
            ('Important Admission Warnings', 'Furnishing false information leads to immediate disqualification. Applicants cannot edit the form after final submission. Selection is strictly based on merit.'),
            ('Login Procedure', 'After creating credentials, applicants should log in using their registered Email ID and Password. Upon logging in, they will be redirected to the dashboard to apply for their respective programmes.'),
            ('Fees Structure','BCA FOR SUBSIDIESED SEAT AROUND 12,760 ,BCA FOR NON SUBSIDIES SEAT AROUND 26,000,BA FOR AROUND 1500,BBA FOE SUBSIDIES AROUND 9,000,BBA FOR NON SUBSIDIES SEAT AROUND 18,000,BSC FOR 1800 AOUND,BVOC FOR AROUND 12000 FOR ALL COURSES IN BVOC ,BCOM FOR AROUND 1600,PGDC FOR 8,000')
      
        
        ]

        print("\n--- Synchronizing College Knowledge Base ---")
        for category, content in college_data:
            # to ensure that data in tabel
            cursor.execute("SELECT id FROM college_info WHERE category = %s", (category,))
            if cursor.fetchone():
                print(f"⚠️  Already Exists: '{category}'")
            else:
                # create new row if not exsist
                cursor.execute("INSERT INTO college_info (category, content) VALUES (%s, %s)", (category, content))
                print(f"✅  Newly Added: '{category}'")

        db.commit()
        db.close()
        print("\n🚀 Database Setup and Sync Completed Successfully!")

    except Exception as e:
        print(f"❌ Error during database setup: {e}")

if __name__ == "__main__":
    update_database_safely()