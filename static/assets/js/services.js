const ENDPOINT_URL = '/system/services/';
const INTERVAL_MS = 2000; // 3 seconds

// Helper function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Get the token once when the script starts
const CSRF_TOKEN = getCookie('csrftoken');
async function sendPostRequest(retryCount = 0) {
    const requestData = {
        'status_check': true,
        'timestamp': new Date().toISOString()
    };
    const response = await fetch(ENDPOINT_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN 
        },
        body: JSON.stringify(requestData)
    });
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}`);
    }
    const responseData = await response.json();
    handleResponse(responseData);
    // Schedule the next request
    setTimeout(() => sendPostRequest(0), INTERVAL_MS);
}
function handleResponse(data) {
    if (data.toast) {
        var toast=data.toast;
        toast.forEach(t=>{
            showToast(t.title,t.message,t.type,t.icon,t.timestamp, t.time_since);
        }
        );}
}
sendPostRequest();