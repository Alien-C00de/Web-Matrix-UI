# Web Matrix UI - Unveil the Secrets of the Website!

### Unveil the Secrets of Your Website: Secure, Analyze, Optimize.
- Web Matrix UI is a comprehensive tool and web application designed to uncover details about a website and provide users with a secure login experience.

- Users can now sign up and create accounts to access the platform.

- The web interface supports Dark & Light mode reports, offering a modern and user-friendly dashboard.

- The main idea is straightforward: provide a URL to the tool, and it will collect, organize, and display a wide range of open data for exploration.

- This data helps identify potential vulnerabilities in the website and optimize configurations. Further fine-tuning reduces the website’s potential risks.

## Features
- Developed in **Python programming**.

- Built with **asynchronous programming**, allowing modules to run in parallel for faster results.

- Includes an **NMAP scan feature** — reports can be generated with or without the NMAP scan.

- Based on the output of each module, it calculates a percentage score for each module and an overall performance score. This is used to **display Website Health**.

- Now available as a **web application with authentication** (sign up & login).

- Supports **Dark & Light mode reports** for better accessibility and user experience.

- Currently, the HTML report **dashboard supports 36 modules**, with more features coming soon!
  
  `1. SSL certificates`
  `2. DNS Records`
  `3. Cookies`
  `4. Crawl Rules`
  `5. Headers`
  `6. Server Location`
  `7. Associated Hosts`
  `8. Redirect Chain`
  `9. TXT Records`
  `10. Server Status`
  `11. Open Ports`  
  `12. Carbon Footprint`
  `13. Server Info`
  `14. Whois Lookup`
  `15. DNS Security Extensions`  
  `16. Site Features`
  `17. DNS Server`
  `18. Tech Stack`
  `19. Security.txt`
  `20. Social Tags`  
  `21. Mail Configuration`
  `22. Firewall Detection`
  `23. HTTP Security Features`
  `24. Archive History`
  `25. Global Ranking`
  `26. Block Detection`
  `27. Malware & Phishing Detection`
  `28. TLS Cipher Suites`  
  `29. Nmap Scan OS Detection`
  `30. Nmap_Scan Version Result`
  `31. NMAP HTTP Vulenrability`
  `32. NMAP SQL Injection`
  `33. NMAP XSS Vulnerability`
  `34. NMAP ShellShock`  
  `35. NMAP RCE Exploit`
  `36. NMAP Web Server Check`       

## Installation
To install and run the Web Matrix UI tool, follow these steps:

Install the required Python libraries:
1. `pip install python-whois`
2. `pip install requests`
3. `pip install asyncio`
4. `pip install aiohttp`
5. `pip install configparser`
6. `pip install colorama`
7. `pip install dnspython`
8. `pip install scapy`
9. `pip install beautifulsoup4`
10. `pip install pybase64`
11. `pip install tldextract`
12. `pip install pyfiglet`
13. `pip install pyOpenSSL`
14. `pip install python3-nmap - Ensure that the nmap software is installed on your machine.`
15. `pip install Flask`
16. `pip install Flask-SQLAlchemy`
17. `pip install Flask-WTF`
18. `pip install Flask-Login`
19. `pip install Flask-Security-Too`

## Usage

### Web Application

  - **Execute the tool using the following commands:**
    ```bash
    python app.py -s google.com -m 0
    ```

  -  **Start the web application server.**

  -  **Users can sign up and log in to access the dashboard.**

  -  **Reports can be viewed in Dark or Light mode.**


## Files

- `./config/config.ini`: This file contains API keys and URL links. Please obtain your API key to run the program.

## Report Files

HTML report files are located under the `web_matrix/Tool/output` directory:

`e.g. WebMatrix_google.com_21Sep2025_20-49-35.html`

## Image
- **Input Screen:**
  <img width="1222" height="721" alt="Screenshot from 2025-09-21 20-49-31" src="https://github.com/user-attachments/assets/08020aef-18ab-4d6e-aded-668c3231c668" />

- **HTML Summary Report Screenshot:**

  <img width="1802" height="996" alt="Screenshot from 2025-09-21 20-55-40" src="https://github.com/user-attachments/assets/c43c68c4-8bbb-40e2-8110-2cc80826e288" />

- **HTML Analysis Report Screenshot**

  <img width="1830" height="1003" alt="Screenshot from 2025-09-21 20-55-58" src="https://github.com/user-attachments/assets/54b8090e-d304-4a89-a5b9-50546e95c723" />


🚀 Happy Website analysis! 🚀
