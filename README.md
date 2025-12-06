# EcoTech Solutions Management System

This i project was made for my oop class.

This is a comprehensive employee, project, and economic indicators management system for EcoTech Solutions, developed with Python and MySQL, implementing security best practices and object-oriented programming.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Security](#security)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Academic Context](#academic-context)
- [Author](#author)

## Description

EcoTech Solutions is a growing company specializing in sustainable technologies. This system was developed to efficiently manage its workforce, projects, and provide access to relevant economic indicators for decision-making.

The system implements a robust security model that includes:

- User authentication with bcrypt (includes salt)
- AES-128 encryption of sensitive data
- Secure external API consumption
- Persistent and secure storage

## Features

### Employee Management

- Employee registration with encrypted data (address, phone, email)
- List and search employees
- Update information
- Deletion with confirmation

### User Management

- Secure authentication system with bcrypt
- User roles (admin, user, manager)
- Salted password hashing
- Role-based authorization

### Department Management

- Create and manage departments
- Assign managers and employees
- Link with projects

### Project Management

- Project registration with start and end dates
- Detailed project descriptions
- Status tracking

### Time Tracking

- Log hours worked by employee and project
- Query by employee or project
- Calculate total hours

### Economic Indicators

- Real-time query of Chilean economic indicators
- Available indicators:
  - Development Unit (UF)
  - Average Value Index (IVP)
  - Consumer Price Index (CPI)
  - Monthly Tax Unit (UTM)
  - Observed Dollar
  - Euro
- Query by specific date or period
- Store queries in database
- User query history

## Technologies Used

- **Python 3.8+**: Main programming language
- **MySQL 8.0+**: Relational database
- **mysql-connector-python**: MySQL connector for Python
- **cryptography**: Library for AES-128 encryption
- **bcrypt**: Library for secure password hashing with salt
- **requests**: HTTP client for API consumption

## Prerequisites

Before starting, make sure you have installed:

- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ecotech-solutions.git
cd ecotech-solutions
```

### 2. Create virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:

```
mysql-connector-python==8.0.33
cryptography==41.0.3
bcrypt==4.1.2
requests==2.31.0
```

### 4. Configure MySQL

Make sure MySQL is running and update the configuration in `conexiondb.py`:

```python
self.__host = "localhost"
self.__port = 3308  # Adjust according to your configuration
self.__user = "root"
self.__password = ""  # Set your password
self.__database = "Ecotech_solutions_DB"
```

### 5. Run the system

```bash
python main.py
```

The system will automatically create the database and necessary tables on first run.

## Usage

### Main Menu

When starting the system, you'll see the main menu with the following options:

```
============================================================
    ECOTECH SOLUTIONS MANAGEMENT SYSTEM
============================================================
1.  Employee Management
2.  User Management
3.  Department Management
4.  Project Management
5.  Time Tracking
6.  Economic Indicators
0.  Exit System
============================================================
```

### Example: Query Economic Indicators

1. Select option `6` from the main menu
2. Choose `1` to query by specific date
3. Select desired indicator (1-6)
4. Enter date in `YYYY-MM-DD` format
5. System will display the indicator value
6. Optionally, you can save the query to the database

### Example: Register an Employee

1. Select option `1` from the main menu
2. Choose `1` to register new employee
3. Enter requested data:
   - Full name
   - Address (will be encrypted automatically)
   - Phone (will be encrypted automatically)
   - Email (will be encrypted automatically)
   - Salary

### Example: Create a User

1. Select option `2` from the main menu
2. Choose `1` to register new user
3. Enter requested data:
   - Username
   - Password (will be hashed with bcrypt and salt)
   - Role (admin/user/manager)
   - Employee ID (optional)

## Project Structure

```
ecotech-solutions/
│
├── main.py                 # System entry point
├── conexiondb.py          # Database connection management
├── clases.py              # Main classes (Employees, User, etc.)
├── indicadores.py         # Economic indicators module
├── requirements.txt       # Project dependencies
├── README.md             # This file
│
└── .gitignore            # Files to ignore in git
```

### Module Description

#### conexiondb.py

- `Database` class: Handles MySQL connection
- Automatic database and table creation
- Connection lifecycle management
- Transaction handling

#### clases.py

- `Empleados`: Employee management with AES-128 encryption for sensitive fields
- `Usuario`: Authentication with bcrypt and authorization with roles
- `Departamento`: Department management
- `Proyecto`: Project management
- `RegistroDeTiempo`: Time tracking and reporting

#### indicadores.py

- `IndicadorEconomico`: Query and store economic indicators
- Integration with mindicador.cl API
- JSON deserialization
- Comprehensive exception handling

#### main.py

- Console-based user interface
- Interactive menus for all operations
- Application main flow and navigation

## Security

### Password Security with bcrypt

The system uses **bcrypt** for password hashing, which provides:

**Automatic Salt Generation**: Each password gets a unique salt

```python
import bcrypt

def _hash_password(password):
    """Generate bcrypt hash with automatic salt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt)
```

**Secure Password Verification**:

```python
def autenticar(self):
    """Authenticate user with bcrypt"""
    stored_hash = resultado['password_hash']
    if bcrypt.checkpw(self.password.encode('utf-8'), stored_hash.encode('utf-8')):
        # Authentication successful
```

**Key Features**:

- Salt is automatically generated and stored with the hash
- Configurable work factor (currently 12 rounds)
- Resistant to rainbow table attacks
- Computationally expensive to slow down brute-force attacks

### Sensitive Data Encryption

The system implements **AES-128-ECB** to encrypt sensitive employee data:

**Encrypted Fields**:

- Employee address
- Employee phone number
- Employee email

**Encryption Implementation**:

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

AES_KEY = b'Mi_Clave_AES_128'  # 16-byte key for AES-128

def _aes_encrypt_ecb(plaintext: str) -> bytes:
    """Encrypt text with AES-128-ECB + PKCS7 padding"""
    # Implementation details in clases.py
```

**Important**: In production, change the AES key and consider using a more secure mode like AES-GCM.

### SQL Injection Prevention

All database queries use parameterized statements:

```python
cursor.execute(
    "SELECT * FROM Usuario WHERE nombre_usuario = %s",
    (self.nombre_usuario,)
)
```

### Input Validation

The system validates all user inputs before processing:

- Date format validation
- Numeric input validation
- Required field checking
- Role validation

## API Documentation

### External API: mindicador.cl

The system consumes the Chilean economic indicators API provided by mindicador.cl.

**Base URL**: `https://mindicador.cl/api`

**Authentication**: Public API, no authentication required

#### Endpoints Used

1. **Get indicator by specific date**

   ```
   GET /api/{indicator}/{dd-mm-yyyy}
   ```

   Example: `https://mindicador.cl/api/uf/06-12-2024`

2. **Get indicator time series**
   ```
   GET /api/{indicator}
   ```
   Example: `https://mindicador.cl/api/dolar`

#### Supported Indicators

| Code    | Indicator | Description                          |
| ------- | --------- | ------------------------------------ |
| `uf`    | UF        | Development Unit (Unidad de Fomento) |
| `ivp`   | IVP       | Average Value Index                  |
| `ipc`   | IPC       | Consumer Price Index                 |
| `utm`   | UTM       | Monthly Tax Unit                     |
| `dolar` | USD       | Observed Dollar                      |
| `euro`  | EUR       | Euro                                 |

#### Response Format

```json
{
  "codigo": "uf",
  "nombre": "Unidad de fomento (UF)",
  "unidad_medida": "Pesos",
  "serie": [
    {
      "fecha": "2024-12-06T04:00:00.000Z",
      "valor": 37500.5
    }
  ]
}
```

### Exception Handling

The system implements comprehensive exception handling for API calls:

```python
try:
    response = requests.get(url, headers=self.headers, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timeout - server took too long to respond")
except requests.exceptions.RequestException as e:
    print(f"Error querying API: {e}")
except json.JSONDecodeError:
    print("Error parsing JSON response")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Database Schema

### Entity Relationship Diagram

```
Empleados (1) ----< (1) Usuario
    |
    |
    v
Departamentos >---- Proyectos
    ^                  ^
    |                  |
    +------ RegistrodeTiempo
                |
                v
        IndicadoresEconomicos >---- Usuario
```

### Tables

#### 1. Empleados (Employees)

```sql
CREATE TABLE Empleados (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion BLOB NOT NULL,           -- AES-128 encrypted
    telefono BLOB NOT NULL,            -- AES-128 encrypted
    email BLOB NOT NULL,               -- AES-128 encrypted
    fecha_contratacion DATE DEFAULT (CURRENT_DATE),
    salario DECIMAL(10,2) NOT NULL
);
```

#### 2. Usuario (Users)

```sql
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt hash with salt
    rol VARCHAR(50),
    id_empleado INT UNIQUE,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado)
        ON DELETE CASCADE
);
```

#### 3. Departamentos (Departments)

```sql
CREATE TABLE Departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gerente VARCHAR(100),
    id_empleado INT,
    id_proyecto INT,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado)
        ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id_proyecto)
        ON DELETE CASCADE
);
```

#### 4. Proyectos (Projects)

```sql
CREATE TABLE Proyectos (
    id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_termino DATE
);
```

#### 5. RegistrodeTiempo (Time Records)

```sql
CREATE TABLE RegistrodeTiempo (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    horas INT NOT NULL,
    descripcion TEXT,
    id_empleado INT NOT NULL,
    id_proyecto INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado)
        ON DELETE CASCADE,
    FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id_proyecto)
        ON DELETE CASCADE
);
```

#### 6. IndicadoresEconomicos (Economic Indicators)

```sql
CREATE TABLE IndicadoresEconomicos (
    id_indicador INT AUTO_INCREMENT PRIMARY KEY,
    nombre_indicador VARCHAR(50) NOT NULL,
    fecha_valor DATE NOT NULL,
    valor DECIMAL(15,4) NOT NULL,
    fecha_consulta DATETIME NOT NULL,
    usuario_consulta VARCHAR(100),
    sitio_proveedor VARCHAR(255),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
        ON DELETE SET NULL
);
```

## Key Features

### Object-Oriented Programming

- Clear class hierarchy with single responsibility principle
- Encapsulation of sensitive data with private attributes
- Properties for controlled access to encrypted fields
- Static methods for utility functions
- Class methods for factory operations

### Security Best Practices

- bcrypt password hashing with automatic salt generation
- AES-128 encryption for sensitive personal data
- SQL injection prevention through parameterized queries
- Input validation and sanitization
- Role-based access control (RBAC)
- Secure session management

### API Integration

- RESTful API consumption with requests library
- JSON deserialization and data validation
- Configurable timeout handling
- Comprehensive error handling and logging
- Graceful degradation on API failures

### Database Design

- Normalized schema (3NF)
- Foreign key constraints for referential integrity
- Cascade deletion for related records
- Transaction management with rollback support
- Indexed primary keys for performance

## Academic Context

This project was developed as part of the **TI3021 - Secure Object-Oriented Programming** course at INACAP, specifically for **Summative Evaluation 3 (ES3)**.

### Learning Objectives

The project demonstrates competency in:

- Implementing secure authentication systems
- Consuming external APIs and web services
- Applying cryptographic techniques (hashing and encryption)
- Designing and implementing object-oriented solutions
- Managing persistent data in relational databases
- Handling exceptions and errors gracefully

### Evaluation Criteria Met

**3.1.1 - Authentication and Security**

- 3.1.1.1: Effective user authentication system with secure credential handling
- 3.1.1.2: Efficient API integration with security standards compliance
- 3.1.1.3: Proper use of hash functions (bcrypt with salt) for sensitive data
- 3.1.1.4: Secure data storage with encryption (AES-128)

**3.1.2 - Library Implementation and Exception Handling**

- 3.1.2.5: Correct implementation of libraries for external data consumption
- 3.1.2.6: Exception handling during program execution
- 3.1.2.7: Secure authentication when interacting with external APIs
- 3.1.2.8: Efficient data storage according to requirements

**3.1.3 - Deserialization and API Consumption**

- 3.1.3.9: Python class for JSON deserialization
- 3.1.3.10: Competent API consumption integration per requirements

**3.1.4 - Database Integration**

- 3.1.4.11: Coherent database structure with proper data modeling
- 3.1.4.12: Compliance with functional and non-functional requirements

## Future Enhancements

- Web interface using Flask or Django framework
- REST API for mobile application integration
- Export functionality for reports (PDF, Excel, CSV)
- Email notification system for important events
- Multi-language support (internationalization)
- Advanced reporting and analytics dashboard
- Two-factor authentication (2FA)
- Audit logging for security events
- Docker containerization for easy deployment
- Unit and integration test suite
- CI/CD pipeline implementation
- PostgreSQL support as alternative database

## Author

**Your Name**

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/your-profile)
- Email: your.email@example.com
- University: INACAP

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **INACAP** - Academic institution providing the educational framework
- **mindicador.cl** - For providing free access to economic indicators API
- **Python Software Foundation** - For the excellent Python language and ecosystem
- **MySQL Community** - For the robust database management system
- **bcrypt Contributors** - For the secure password hashing library
- **Course Instructor** - For guidance and requirements specification

## Support and Contact

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/your-username/ecotech-solutions/issues) section
2. Create a new issue with detailed information
3. Contact via email with subject line: "EcoTech Solutions Support"

## Disclaimer

This is an academic project developed for educational purposes. While it implements security best practices, it should undergo a professional security audit before being used in production environments.

**Security Notes**:

- Change all default keys and passwords before production use
- Implement HTTPS for all network communications
- Consider using environment variables for sensitive configuration
- Implement rate limiting for API endpoints
- Add comprehensive logging and monitoring
- Regular security updates for all dependencies

---

**Project Status**: Active Development  
**Version**: 1.0.0  
**Last Updated**: December 2024  
**Institution**: INACAP  
**Course**: TI3021 - Secure Object-Oriented Programming
