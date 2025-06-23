#!/usr/bin/env python3
"""
Script to fix invalid password hashes in the database
Run this to regenerate all password hashes with proper bcrypt format
"""

import psycopg2
import bcrypt
import traceback

def fix_password_hashes():
    print("=== Fixing Password Hashes ===")
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host='postgres_shared',
            database='users_DB',
            user='postgres',
            password='Seventrees',
            port='5432'
        )
        cursor = conn.cursor()
        
        # Get all users and their current hashes
        cursor.execute("SELECT id, email, password_hash, first_name FROM users")
        users = cursor.fetchall()
        
        print(f"Found {len(users)} users to fix")
        
        # Define default passwords for each user (change these as needed)
        user_passwords = {
            'alice.adams@gmail.com': 'alice123',
            'bob.brown@gmail.com': 'bob123', 
            'charlie.clark@gmail.com': 'charlie123',
            'jacco.jones@gmail.com': 'jacco123',
            'stephen.smith@gmail.com': 'stephen123',
            'leon.lewis@gmail.com': 'leon123',
            'celina.carter@gmail.com': 'celina123',
            'test@example.com': 'test123',
            'test@test.com': 'test123'
        }
        
        for user_id, email, current_hash, first_name in users:
            print(f"\n👤 Processing {email} ({first_name})")
            print(f"   Current hash: {current_hash[:30]}...")
            
            # Check if current hash is valid bcrypt
            is_valid_bcrypt = current_hash.startswith(('$2a$', '$2b$', '$2y$')) and len(current_hash) == 60
            print(f"   Valid bcrypt format: {'✅' if is_valid_bcrypt else '❌'}")
            
            # Get password for this user
            if email in user_passwords:
                new_password = user_passwords[email]
            else:
                # Default password based on first name
                new_password = f"{first_name.lower()}123"
            
            print(f"   Setting password: {new_password}")
            
            # Generate new bcrypt hash
            new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(f"   New hash: {new_hash[:30]}...")
            
            # Update database
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (new_hash, user_id)
            )
            
            # Verify the new hash works
            test_verify = bcrypt.checkpw(new_password.encode('utf-8'), new_hash.encode('utf-8'))
            print(f"   Verification: {'✅ Success' if test_verify else '❌ Failed'}")
        
        # Commit all changes
        conn.commit()
        print(f"\n✅ Successfully updated {len(users)} user passwords")
        
        # Test one user to make sure everything works
        test_email = 'test@example.com'
        test_password = 'test123'
        
        cursor.execute("SELECT password_hash FROM users WHERE email = %s", (test_email,))
        result = cursor.fetchone()
        
        if result:
            stored_hash = result[0]
            final_test = bcrypt.checkpw(test_password.encode('utf-8'), stored_hash.encode('utf-8'))
            print(f"\n🧪 Final test ({test_email} with '{test_password}'): {'✅ PASS' if final_test else '❌ FAIL'}")
        
        cursor.close()
        conn.close()
        
        print("\n📋 Updated User Credentials:")
        for email, password in user_passwords.items():
            print(f"   {email} : {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing passwords: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def create_test_users():
    """Create additional test users with known good passwords"""
    print("\n=== Creating Test Users ===")
    
    try:
        conn = psycopg2.connect(
            host='postgres_shared',
            database='users_DB',
            user='postgres',
            password='Seventrees',
            port='5432'
        )
        cursor = conn.cursor()
        
        test_users = [
            ('admin@test.com', 'admin123', 'Admin', 'User', 1),
            ('user@test.com', 'user123', 'Regular', 'User', 0),
            ('demo@test.com', 'demo123', 'Demo', 'User', 0)
        ]
        
        for email, password, first_name, last_name, role_id in test_users:
            # Generate bcrypt hash
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert or update user
            cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, role_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO UPDATE SET
                    password_hash = EXCLUDED.password_hash,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    role_id = EXCLUDED.role_id
            """, (email, password_hash, first_name, last_name, role_id, True))
            
            print(f"✅ Created/Updated {email} (password: {password})")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test users: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Password Hash Repair Tool")
    print("=" * 50)
    
    success1 = fix_password_hashes()
    success2 = create_test_users()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ All password hashes fixed successfully!")
        print("\n🚀 You can now test login with:")
        print("   Email: test@example.com, Password: test123")
        print("   Email: admin@test.com, Password: admin123")
        print("   Email: alice.adams@gmail.com, Password: alice123")
    else:
        print("❌ Some operations failed. Check errors above.")