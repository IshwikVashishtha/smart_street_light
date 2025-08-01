# Streetlight Management System

A comprehensive Django REST API for managing IoT-enabled streetlight devices with real-time monitoring, control, and alerting capabilities.

## 🚀 Features

- **Device Management**: Register and manage streetlight devices
- **Real-time Monitoring**: Track voltage, current, power, and energy consumption
- **Remote Control**: Turn devices ON/OFF remotely with duration control
- **Scheduling**: Set up automated on/off schedules for devices
- **Alert System**: Email notifications for low power conditions
- **JWT Authentication**: Secure API access with token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled for frontend integration

## 🏗️ Architecture

This project follows a Django REST API architecture with the following components:

- **Django 5.2.4**: Web framework
- **Django REST Framework**: API development
- **JWT Authentication**: Secure token-based authentication
- **SQLite Database**: Lightweight database for development
- **CORS Headers**: Cross-origin request handling

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (for version control)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd streetlight
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file in the root directory with the following content:

```txt
Django==5.2.4
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

### 4. Navigate to Django Project

```bash
cd config
```

### 5. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Authentication Required Endpoints

#### Register Device
```http
POST /api/register_device
Content-Type: application/json
Authorization: Bearer <your-jwt-token>

{
    "device_id": "SL001",
    "location": "Main Street, Downtown",
    "total_lights": 10,
    "estimated_load": 1000.0
}
```

#### List All Devices
```http
GET /api/list_devices
Authorization: Bearer <your-jwt-token>
```

#### Control Device
```http
POST /api/control_device
Content-Type: application/json
Authorization: Bearer <your-jwt-token>

{
    "device_id": "SL001",
    "command": "ON",
}
```

### Public Endpoints

#### Report Device Data
```http
POST /api/report_data
Content-Type: application/json

{
    "device": 1,
    "voltage": 220.0,
    "current": 4.5,
    "power": 990.0,
    "energy": 15.5,
    "status": "ON"
}
```

#### Get Device Command
```http
GET /api/get_command?device_id=SL001
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. To get a token:

1. Create a superuser account
2. Use Django admin interface or implement a login endpoint
3. Include the token in the Authorization header: `Bearer <your-token>`

## 🗄️ Database Models

### Device
- `device_id`: Unique identifier for the device
- `location`: Physical location of the device
- `total_lights`: Number of lights in the device
- `estimated_load`: Estimated power load in watts
- `status`: Current status (ON/OFF)

### DeviceData
- `device`: Foreign key to Device
- `voltage`: Voltage reading
- `current`: Current reading
- `power`: Power consumption in watts
- `energy`: Energy consumption
- `status`: Device status at time of reading
- `timestamp`: When the data was recorded

### DeviceCommand
- `device`: One-to-one relationship with Device
- `command`: Command to execute (ON/OFF)
<!-- - `duration`: Duration in minutes -->

### Schedule
- `device`: Foreign key to Device
- `on_time`: Time to turn on
- `off_time`: Time to turn off
- `repeat_daily`: Whether to repeat daily

## 🚨 Alert System

The system automatically sends email alerts when:
- Power consumption drops below 10 watts (configurable threshold)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `config` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### CORS Settings

The API is configured to allow cross-origin requests. Update `ALLOWED_HOSTS` and CORS settings in `settings.py` for production.

<!-- ## 🧪 Testing

Run the test suite:

```bash
python manage.py test
``` -->

## 📦 Deployment

### Production Checklist

1. **Security Settings**:
   - Set `DEBUG = False`
   - Update `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`

2. **Database**:
   - Consider using PostgreSQL for production
   - Set up proper database credentials

3. **Static Files**:
   - Configure static file serving
   - Set up a CDN if needed

4. **Email Configuration**:
   - Configure SMTP settings for alerts

5. **Web Server**:
   - Use Gunicorn or uWSGI
   - Set up Nginx as reverse proxy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

<!-- 1. Check the [Issues](https://github.com/your-repo/issues) page -->
1. Create a new issue with detailed information
2. Contact the development team

<!-- ## 🔄 Version History

- **v1.0.0**: Initial release with basic device management and monitoring
- **v1.1.0**: Added scheduling and alert system
- **v1.2.0**: Enhanced authentication and CORS support -->

---

**Note**: This is a development version. For production use, ensure all security measures are properly configured. 