# BEIJ API Gateway

A centralized API gateway service that acts as a single entry point for frontend applications to communicate with the BEIJ e-commerce backend services.

## Architecture

```
Frontend (React/Vue/Angular) → API Gateway (Port 8000) → Backend Services (Port 8001)
```

## Features

- **Centralized API Access**: Single endpoint for all frontend requests
- **Data Transformation**: Optimizes backend responses for frontend consumption
- **CORS Handling**: Configured for web frontend development
- **Error Handling**: Standardized error responses
- **Request Routing**: Intelligent routing to appropriate backend services
- **Enhanced Endpoints**: Additional frontend-specific functionality

## Quick Start

### 1. Install Dependencies

```bash
cd gateway
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Backend Service

Make sure your backend service is running on port 8001:

```bash
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### 4. Start Gateway

```bash
cd gateway
python main.py
# Or using uvicorn directly:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Test the Gateway

Visit: http://localhost:8000/docs for interactive API documentation

## API Endpoints

### Products
- `GET /api/v1/products` - Get all products (frontend-optimized)
- `GET /api/v1/products/{id}` - Get single product
- `POST /api/v1/products` - Create product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product
- `GET /api/v1/products/search` - Search products with filters

### Users
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - User login
- `POST /api/v1/users/logout` - User logout
- `GET /api/v1/users/profile/{id}` - Get user profile
- `PUT /api/v1/users/profile/{id}` - Update user profile

### Product Previews
- `GET /api/v1/previews` - Get all product previews
- `GET /api/v1/previews/filtered` - Get filtered previews
- `GET /api/v1/previews/categories` - Get available categories
- `GET /api/v1/previews/price-range` - Get price range
- `GET /api/v1/previews/featured` - Get featured products
- `GET /api/v1/previews/search` - Search previews

### Health Checks
- `GET /health` - Gateway health check
- `GET /health/backend` - Backend service health check

## Frontend Integration

### JavaScript/TypeScript Example

```javascript
// Configure your frontend to use the gateway
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Fetch products
const products = await fetch(`${API_BASE_URL}/products`).then(r => r.json());

// User login
const loginResponse = await fetch(`${API_BASE_URL}/users/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'user', password: 'pass' })
}).then(r => r.json());
```

### React Example

```jsx
import { useEffect, useState } from 'react';

function ProductList() {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    fetch('http://localhost:8000/api/v1/products')
      .then(response => response.json())
      .then(data => setProducts(data));
  }, []);
  
  return (
    <div>
      {products.map(product => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <p>${product.price.current}</p>
          <p>Rating: {product.rating.score}/5</p>
        </div>
      ))}
    </div>
  );
}
```

## Data Transformation

The gateway transforms backend data to be more frontend-friendly:

### Backend Product Format:
```json
{
  "product_id": "123",
  "product_name": "Example Product",
  "discounted_price": 29.99,
  "actual_price": 39.99,
  "rating": 4.5,
  "rating_count": 100
}
```

### Frontend Product Format:
```json
{
  "id": "123",
  "name": "Example Product",
  "price": {
    "current": 29.99,
    "original": 39.99,
    "discount": "25%"
  },
  "rating": {
    "score": 4.5,
    "count": 100
  }
}
```

## Configuration

### Environment Variables

- `BACKEND_URL`: URL of the backend service (default: http://localhost:8001)
- `BACKEND_TIMEOUT`: Request timeout in seconds (default: 30)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins
- `GATEWAY_PORT`: Port for the gateway service (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)

### CORS Configuration

The gateway is pre-configured for common frontend development ports:
- http://localhost:3000 (React)
- http://localhost:5173 (Vite)
- http://localhost:8080 (Vue)

## Development

### Project Structure

```
gateway/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── routers/            # API route handlers
│   ├── products.py     # Product endpoints
│   ├── users.py        # User endpoints
│   └── previews.py     # Preview endpoints
└── services/           # Business logic
    └── backend_client.py # HTTP client for backend communication
```

### Adding New Endpoints

1. Add route handler in appropriate router file
2. Implement data transformation if needed
3. Add error handling
4. Update this README

## Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

- Use environment variables for configuration
- Set up proper logging and monitoring
- Configure rate limiting
- Add authentication middleware
- Use HTTPS in production
- Set appropriate CORS origins

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**: Ensure backend service is running on configured port
2. **CORS Errors**: Add your frontend URL to ALLOWED_ORIGINS
3. **Timeout Errors**: Increase BACKEND_TIMEOUT value
4. **Port Conflicts**: Change GATEWAY_PORT in configuration

### Logs

The gateway provides detailed logging for debugging:

```bash
# View logs in real-time
python main.py

# Or with uvicorn
uvicorn main:app --log-level debug
```
