"""
Script to add InputValidationError handler to main.py
Run this script to automatically update main.py with the exception handler.
"""

import re

# Read the current main.py
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Step 1: Add import after PasswordValidationError import
import_pattern = r'(from domain\.models\.exceptions\.password_validation_error import PasswordValidationError\r?\n)'
import_replacement = r'\1from infrastructure.security.input_validators import InputValidationError\r\n'

if 'from infrastructure.security.input_validators import InputValidationError' not in content:
    content = re.sub(import_pattern, import_replacement, content)
    print("✅ Added InputValidationError import")
else:
    print("ℹ️  InputValidationError import already exists")

# Step 2: Add exception handler after PasswordValidationError handler
handler_pattern = r'(@app\.exception_handler\(PasswordValidationError\).*?content=\{\"detail\": str\(exc\)\}\s*\)\s*\)\s*)(.*?@app\.exception_handler\(Exception\))'

handler_replacement = r'''\1
    @app.exception_handler(InputValidationError)
    async def input_validation_exception_handler(request: Request, exc: InputValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )
        
    \2'''

if '@app.exception_handler(InputValidationError)' not in content:
    content = re.sub(handler_pattern, handler_replacement, content, flags=re.DOTALL)
    print("✅ Added InputValidationError exception handler")
else:
    print("ℹ️  InputValidationError handler already exists")

# Write the updated content
with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ main.py updated successfully!")
print("Next step: Run 'docker compose restart backend' to apply changes")
