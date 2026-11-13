import bcrypt

def generate_hash_password(password):
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password.encode(), salt)
  return hashed_password.decode()

def check_password(password, hashed_password):
  try:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
  except ValueError as e:
    print("Error checking password:", e)
    return False