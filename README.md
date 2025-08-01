# Streetlight Management System

A comprehensive IoT streetlight management system with Django REST API backend and React.js frontend for real-time monitoring, control, and scheduling of streetlight devices.

## 🚀 Features

### Backend (Django REST API)
- **Device Management**: Register and manage streetlight devices
- **Real-time Monitoring**: Track voltage, current, power, and energy consumption
- **Remote Control**: Turn devices ON/OFF remotely
- **Scheduling**: Set up automated on/off schedules for devices
- **Alert System**: Email notifications for low power conditions
- **JWT Authentication**: Secure API access with token-based authentication
- **CORS Support**: Cross-origin resource sharing enabled for frontend integration
- **Device Data History**: Historical data tracking and analytics

### Frontend (React.js)
- **Modern UI**: Material-UI based responsive interface
- **Real-time Dashboard**: Live monitoring of all devices
- **Device Control**: Intuitive device management interface
- **Schedule Management**: Create and manage automated schedules
- **Data Visualization**: Charts and graphs for power consumption
- **Authentication**: Secure login with JWT tokens
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Architecture

### Backend Stack
- **Django 5.2.4**: Web framework
- **Django REST Framework**: API development
- **JWT Authentication**: Secure token-based authentication
- **SQLite Database**: Lightweight database for development
- **CORS Headers**: Cross-origin request handling

### Frontend Stack
- **React.js 18**: Frontend framework
- **Vite**: Build tool and development server
- **Material-UI (MUI)**: UI component library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Recharts**: Data visualization library
- **React Context**: State management

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+**
- **npm** or **yarn**
- **Git** (for version control)

## 🛠️ Installation & Setup

### Backend Setup

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd streetlight
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Navigate to Django Project
```bash
cd config
```

#### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create Superuser
```bash
python manage.py createsuperuser
```

#### 7. Run the Backend Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### Frontend Setup

#### 1. Navigate to Frontend Directory
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Start Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173/`

## 📚 API Endpoints

### Authentication Required Endpoints

#### JWT Token Authentication
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

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
    "command": "ON"
}
```

#### Get Device Data (for charts and analytics)
```http
GET /api/device_data/<device_id>
Authorization: Bearer <your-jwt-token>
```

#### Schedule Management
```http
GET /api/list_schedules
POST /api/create_schedule
DELETE /api/delete_schedule/<schedule_id>
Authorization: Bearer <your-jwt-token>
```

### Public Endpoints (for ESP32)

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

The system uses JWT (JSON Web Tokens) for authentication:

1. **Login**: Use your Django superuser credentials
2. **Token**: JWT tokens are automatically managed by the frontend
3. **Security**: All sensitive endpoints require authentication

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

### Schedule
- `device`: Foreign key to Device
- `on_time`: Time to turn on
- `off_time`: Time to turn off
- `repeat_daily`: Whether to repeat daily

## 🚨 Alert System

The system automatically sends email alerts when:
- Power consumption drops below 10 watts (configurable threshold)

## 🔧 Configuration

### Backend Environment Variables

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

### Frontend Configuration

The frontend is configured to connect to the backend at `http://localhost:8000`. Update the API base URL in the context files if needed.

## 📱 Frontend Features

### Pages
- **Dashboard**: Overview of all devices and system statistics
- **Devices**: List and manage all streetlight devices
- **Device Detail**: Detailed view with real-time data and charts
- **Schedules**: Create and manage automated schedules
- **Alerts**: View system alerts and notifications

### Components
- **Responsive Sidebar**: Navigation menu
- **Real-time Charts**: Power consumption and energy usage
- **Device Cards**: Status indicators and quick controls
- **Schedule Forms**: Easy schedule creation and management

<!-- ## 🤖 ESP32 Integration

### Required Endpoints for ESP32
1. **Device Registration**: `POST /api/register_device` (one-time setup)
2. **Data Reporting**: `POST /api/report_data` (regular intervals)
3. **Command Checking**: `GET /api/get_command?device_id=<id>` (polling)

### ESP32 Implementation Example
```cpp
// Send sensor data
void sendSensorData() {
  HTTPClient http;
  http.begin("http://your-server:8000/api/report_data");
  http.addHeader("Content-Type", "application/json");
  
  String jsonData = "{\"device\":\"SL001\",\"voltage\":220.5,\"current\":4.2,\"power\":950.0,\"energy\":15.7,\"status\":\"ON\"}";
  int httpResponseCode = http.POST(jsonData);
  http.end();
}

// Check for commands
String checkCommands() {
  HTTPClient http;
  http.begin("http://your-server:8000/api/get_command?device_id=SL001");
  int httpResponseCode = http.GET();
  String response = http.getString();
  http.end();
  return response;
}
``` -->

## 📦 Deployment

### Production Checklist

#### Backend
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

#### Frontend
1. **Build for Production**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy**:
   - Serve the `dist` folder with a web server
   - Configure environment variables
   - Set up HTTPS

<!-- ## 🧪 Testing

### Backend Testing
```bash
cd config
python manage.py test
```

### Frontend Testing
```bash
cd frontend
npm test
``` -->

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

1. Check the documentation
2. Create a new issue with detailed information
3. Contact the development team

## 🔄 Version History

- **v1.0.0**: Initial release with basic device management
- **v1.1.0**: Added scheduling and alert system
- **v1.2.0**: Enhanced authentication and CORS support
- **v1.3.0**: Added React.js frontend with real-time monitoring
- **v1.4.0**: Complete schedule management and device analytics

---

**Note**: This is a development version. For production use, ensure all security measures are properly configured.