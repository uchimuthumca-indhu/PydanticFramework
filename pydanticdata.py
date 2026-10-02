from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# Define a User Model inheriting from Pydantic's BaseModel
class User(BaseModel):
    # 1. Basic Fields with Type Annotations
    id: int
    name: str = Field(..., min_length=2, description="Name must be at least 2 characters")
    
    # 2. Field Validation with EmailStr (requires 'pydantic[email]' package)
    email: str
    
    # 3. Optional Field with a Default Value
    is_active: bool = True
    
    # 4. Constrained Field using Field()
    # age must be between 18 and 120
    age: int = Field(gt=17, lt=121, description="User must be an adult under 121")
    
    # 5. Nested Collections (List of strings)
    tags: List[str] = []
    
    # 6. Datetime auto-parsing
    signup_timestamp: Optional[datetime] = None

    # 7. Custom Validator
    # Ensures the username/name does not contain forbidden words
    @field_validator("name")
    @classmethod
    def name_must_not_contain_admin(cls, value: str) -> str:
        if "admin" in value.lower():
            raise ValueError("Name cannot contain the word 'admin'")
        return value.title()  # Capitalizes the name nicely


# ==========================================
# 1. SUCCESSFUL VALIDATION EXAMPLE
# ==========================================
print("--- 1. Valid Input Data Example ---")

# Raw data (notice 'age' is a string "25", but Pydantic coerces it to an int 25)
valid_data = {
    "id": "101",  # Coerced from str -> int
    "name": "john doe",  # Will be capitalized by custom validator to 'John Doe'
    "email": "john.doe@example.com",
    "age": "25",  # Coerced from str -> int
    "tags": ["python", "pydantic"],
    "signup_timestamp": "2026-03-30T10:00:00",  # Automatically parsed into datetime object
}

# Instantiate model
user = User(**valid_data)

# Print parsed Python object
print(f"Parsed User ID: {user.id} (Type: {type(user.id)})")
print(f"Formatted Name: {user.name}")
print(f"User Age: {user.age} (Type: {type(user.age)})")
print(f"Created At: {user.signup_timestamp} (Type: {type(user.signup_timestamp)})")

# Export model back to dictionary or JSON
print("\nExported as JSON:")
print(user.model_dump_json(indent=2))


# ==========================================
# 2. VALIDATION FAILURE EXAMPLE
# ==========================================
print("\n--- 2. Invalid Input Data Example ---")

invalid_data = {
    "id": "not_an_number",  # Invalid integer
    "name": "admin_user",  # Violates custom validator
    "email": "invalid-email",
    "age": 15,  # Violates age constraint (must be > 17)
}

try:
    # Attempting to create user with invalid data
    invalid_user = User(**invalid_data)
except Exception as e:
    # Pydantic raises a ValidationError with clear details
    print("Validation Error Caught Successfully!")
    print(e)