# Secure Flask Application

This is a secure Flask application with user authentication, note management, and profile features.

## Security Features Implemented

1. **SQL Injection Prevention**: All database queries use parameterized statements
2. **Input Sanitization**: All user inputs are sanitized to prevent XSS attacks
3. **Secure Password Handling**: Passwords are hashed using bcrypt
4. **Docker Security**: Runs as non-root user with minimal permissions
5. **Secure Docker Image**: Uses Alpine Linux base for minimal attack surface
6. **Image URL Validation**: Profile image URLs are validated for security

## Requirements

- Docker
- Docker Compose

## How to Run

```bash
# Build and start the application
docker-compose up --build

# The application will be available at http://localhost:5000
```

## Default Credentials

- **User**: user@evfa.com / StrongPassword123!
- **Admin**: admin@evfa.com / StrongAdminPassword123!

Registration codes are required to create new accounts. The default static registration code is: `a36e990b-0024-4d55-b74a-f8d7528e1764`

## Features

- User authentication (login/logout)
- Note creation and management
- Profile management with image upload
- Admin panel for registration code management
- Dark/light mode toggle

## Docker Configuration

The application uses a minimal Alpine Linux base image with:
- Non-root user execution
- Only necessary packages installed
- Proper file permissions
- Multi-stage build process

## Security Notes

- In production, change the SECRET_KEY environment variable
- Use strong passwords for default accounts
- Configure ALLOWED_DOMAINS in `utils/profile_image.py` for production image hosting
