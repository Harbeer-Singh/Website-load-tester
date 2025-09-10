# 🚀 Load Testing Script

A Python script to test how a website handles multiple concurrent users.  
It simulates traffic, measures response times, and reports success/failure counts.  
Perfect for checking server performance safely.

---

## 🛠️ Requirements

- **Python 3.8+**  
- **aiohttp library**

Install aiohttp:  
```bash
pip install aiohttp
```

---

## ⚡ Usage

Run the script:  
```bash
python DOS_Attack.py
```

**Enter the input parameters when prompted:**  
- **URL** – the website to test (e.g., http://localhost:8000)  
- **Number of concurrent users** – simulated users sending requests simultaneously  
- **Requests per user** – number of requests each user will send  

**Example output:**  
```
Users: 5, Requests: 25, Success: 25, Fail: 0, Avg Response: 0.134s
```

---

## ⚠️ Important Notes

- Only test websites you own or have permission to test.  
- Start with small numbers to avoid overloading the server.  
- For HTTPS sites, SSL verification is disabled for testing purposes.  

---

## 💡 Tips

- Gradually increase users/requests to see how your server performs under load.  
- Monitor server logs and CPU/memory usage during tests.  
- You can modify the script to log detailed response times or batch requests for safer large-scale testing.

  ## 📸 Screenshots

 **DEMO RUN**  
 ![Intercepted Request]()
