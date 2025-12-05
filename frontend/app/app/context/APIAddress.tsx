const API_BASE = "http://host.docker.internal:8000/api/v1"; //For requests on frontend server(inside docker container)
const API_CLIENT_BASE = "http://localhost:8000/api/v1"; //use localhost for client side requests(outside docker container)

export function BackendAddress(){
    if (typeof window === 'undefined') {
    // Running on server
    return API_BASE;
  } else {
    // Running on client
    return API_CLIENT_BASE;
  }
}

export { API_BASE};
export { API_CLIENT_BASE };