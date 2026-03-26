from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import urllib.parse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
C_EXEC = os.path.join(BASE_DIR, "attendance")

print("BASE_DIR:", BASE_DIR)
print("C_EXEC:", C_EXEC)

def page_layout(content, title=""):
    return f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Smart Attendance Manager</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">

    <style>
    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        font-family: 'Poppins', sans-serif;
        background: #0b0b0b;
        color: #f5f5f5;
    }}

    .header {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 78px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 28px;
        background: #111111;
        border-bottom: 1px solid #222222;
        z-index: 1000;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 22px;
        font-weight: 700;
        color: #f5f5f5;
    }}

    .brand-cap {{
        font-size: 36px;
        color: #e6d3a3;
        filter: grayscale(1) brightness(1.1);
    }}

    .sidebar {{
        position: fixed;
        top: 78px;
        left: 0;
        width: 240px;
        height: calc(100vh - 78px);
        background: #0f0f0f;
        border-right: 1px solid #222222;
        padding: 22px 16px;
    }}

    .sidebar a {{
        display: block;
        padding: 12px 14px;
        margin: 10px 0;
        color: #d9d9d9;
        text-decoration: none;
        border-radius: 12px;
        transition: 0.25s ease;
        background: #151515;
        border: 1px solid #222;
    }}

    .sidebar a:hover {{
        background: #e6d3a3;
        color: #000000;
        transform: translateX(6px);
    }}

    .main {{
        margin-left: 240px;
        padding: 108px 34px 34px;
    }}

    h1 {{
        margin-top: 0;
        margin-bottom: 20px;
        font-size: 30px;
        color: #f5f5f5;
    }}

    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 18px;
        margin-bottom: 22px;
    }}

    .card {{
        background: #151515;
        border: 1px solid #222222;
        border-radius: 16px;
        padding: 22px;
        transition: 0.25s ease;
    }}

    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 0 18px rgba(230, 211, 163, 0.16);
    }}

    .stat-label {{
        font-size: 14px;
        color: #bfbfbf;
        margin-bottom: 8px;
    }}

    .stat-value {{
        font-size: 34px;
        font-weight: 700;
        color: #e6d3a3;
    }}

    h2, h3 {{
        margin-top: 0;
        color: #f5f5f5;
    }}

    input {{
        width: 100%;
        padding: 12px;
        margin: 8px 0 14px;
        border-radius: 10px;
        border: 1px solid #333333;
        background: #0f0f0f;
        color: #ffffff;
        outline: none;
    }}

    input:focus {{
        border-color: #e6d3a3;
        box-shadow: 0 0 0 2px rgba(230, 211, 163, 0.18);
    }}

    button {{
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 10px;
        background: #e6d3a3;
        color: #000000;
        font-weight: 700;
        cursor: pointer;
        transition: 0.25s ease;
    }}

    button:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 16px rgba(230, 211, 163, 0.24);
    }}

    .danger-btn {{
        background: #1b1b1b;
        color: #f5f5f5;
        border: 1px solid #444;
    }}

    .danger-btn:hover {{
        background: #8b4a4a;
        color: #ffffff;
        box-shadow: 0 0 14px rgba(139, 74, 74, 0.22);
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 14px;
        background: #ffffff;
        color: #000000;
        border-radius: 12px;
        overflow: hidden;
    }}

    th {{
        background: #111111;
        color: #ffffff;
        padding: 14px;
        font-size: 14px;
    }}

    td {{
        padding: 13px;
        text-align: center;
        border-bottom: 1px solid #ececec;
    }}

    tr:nth-child(even) {{
        background: #f4f4f4;
    }}

    tr:hover {{
        background: #ece7db;
    }}

    .green-row {{
        background: #dfe9dd !important;
        color: #2f4f3a !important;
        font-weight: 600;
    }}

    .red-row {{
        background: #eadede !important;
        color: #6d3f3f !important;
        font-weight: 600;
    }}

    .low-row {{
        background: #eadede !important;
        color: #6d3f3f !important;
        font-weight: 700;
    }}

    .result-box {{
        background: #101010;
        border: 1px solid #2c2c2c;
        border-radius: 14px;
        padding: 18px;
        white-space: pre-wrap;
        line-height: 1.7;
        color: #f5f5f5;
    }}

    .back-link {{
        display: inline-block;
        margin-top: 16px;
        text-decoration: none;
        color: #e6d3a3;
        font-weight: 600;
    }}
    </style>
    </head>

    <body>
        <div class="header">
            <div class="brand">
                <span class="brand-cap">🎓</span>
                <span>Smart Attendance Manager</span>
            </div>
            <span class="brand-cap">🎓</span>
        </div>

        <div class="sidebar">
            <a href="/">Dashboard</a>
            <a href="/display">Students</a>
            <a href="/attendance">Attendance</a>
            <a href="/shortage">Shortage</a>
            <a href="/summary">Summary</a>
        </div>

        <div class="main">
            <h1>{title}</h1>
            {content}
        </div>
    </body>
    </html>
    """

def run_c(args):
    try:
        cmd = [os.path.abspath(C_EXEC)] + args
        print("RUNNING:", cmd)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=5
        )

        if result.returncode != 0:
            return f"⚠️ Error:\n{result.stderr}"

        return result.stdout if result.stdout else "Done"

    except subprocess.TimeoutExpired:
        return "⚠️ Error:\nC program timed out."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def count_students_from_display(display_output):
    lines = [line.strip() for line in display_output.strip().split("\n") if line.strip()]
    if len(lines) <= 1:
        return 0
    return len(lines) - 1

class AppHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            display_output = run_c(["display"])
            total_students = 0 if display_output.startswith("⚠️ Error") else count_students_from_display(display_output)

            content = f"""
            <div class="grid">
                <div class="card">
                    <div class="stat-label">Total Students</div>
                    <div class="stat-value">{total_students}</div>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <h3>Add Student</h3>
                    <form action="/add" method="get">
                        <input name="reg" placeholder="Register Number" required>
                        <input name="name" placeholder="Student Name" required>
                        <button>Add Student</button>
                    </form>
                </div>

                <div class="card">
                    <h3>Mark Attendance</h3>
                    <form action="/mark" method="get">
                        <input name="reg" placeholder="Register Number" required>
                        <input name="status" placeholder="P / A" required>
                        <button>Submit Attendance</button>
                    </form>
                </div>

                <div class="card">
                    <h3>Remove Student</h3>
                    <form action="/remove" method="get">
                        <input name="reg" placeholder="Register Number" required>
                        <button class="danger-btn">Remove Student</button>
                    </form>
                </div>
            </div>
            """
            self.respond(page_layout(content, "Dashboard"))

        elif path == "/add":
            reg = query.get("reg", [""])[0].strip()
            name = query.get("name", [""])[0].strip()

            if not reg or not name:
                self.message("Please enter both Register Number and Student Name.")
                return

            self.message(run_c(["add", reg, name]))

        elif path == "/remove":
            reg = query.get("reg", [""])[0].strip()

            if not reg:
                self.message("Please enter a Register Number.")
                return

            self.message(run_c(["remove", reg]))

        elif path == "/mark":
            reg = query.get("reg", [""])[0].strip()
            status = query.get("status", [""])[0].strip()

            if not reg or not status:
                self.message("Please enter both Register Number and attendance status.")
                return

            self.message(run_c(["mark", reg, status]))

        elif path == "/display":
            output = run_c(["display"])
            rows = ""

            for line in output.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) >= 4:
                    rows += f"<tr><td>{parts[0]}</td><td>{' '.join(parts[1:-2])}</td><td>{parts[-2]}</td><td>{parts[-1]}</td></tr>"

            content = f"""
            <div class='card'>
                <h2>Students</h2>
                <table>
                    <tr><th>RegNo</th><th>Name</th><th>Total</th><th>Present</th></tr>
                    {rows}
                </table>
            </div>
            """
            self.respond(page_layout(content, "Students"))

        elif path == "/attendance":
            output = run_c(["attendance"])
            rows = ""

            for line in output.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    percent = float(parts[-1])

                    if percent >= 75:
                        row_class = "green-row"
                    else:
                        row_class = "red-row"

                    rows += f"<tr class='{row_class}'><td>{parts[0]}</td><td>{' '.join(parts[1:-1])}</td><td>{parts[-1]}</td></tr>"

            content = f"""
            <div class='card'>
                <h2>Attendance</h2>
                <table>
                    <tr><th>RegNo</th><th>Name</th><th>%</th></tr>
                    {rows}
                </table>
            </div>
            """
            self.respond(page_layout(content, "Attendance"))

        elif path == "/shortage":
            output = run_c(["shortage"])
            rows = ""

            for line in output.strip().split("\n")[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    rows += f"<tr class='low-row'><td>{parts[0]}</td><td>{' '.join(parts[1:-1])}</td><td>{parts[-1]}</td></tr>"

            content = f"""
            <div class='card'>
                <h2>Shortage</h2>
                <table>
                    <tr><th>RegNo</th><th>Name</th><th>%</th></tr>
                    {rows}
                </table>
            </div>
            """
            self.respond(page_layout(content, "Shortage"))

        elif path == "/summary":
            output = run_c(["summary"])
            content = f"""
            <div class='card'>
                <h2>Summary</h2>
                <div class='result-box' style='text-align:center;font-size:26px;font-weight:700;'>{output}</div>
            </div>
            """
            self.respond(page_layout(content, "Summary"))

        else:
            self.message("Page not found")

    def message(self, msg):
        content = f"""
        <div class='card'>
            <h2>Result</h2>
            <div class='result-box'>{msg}</div>
            <a class='back-link' href='/'>⬅ Back</a>
        </div>
        """
        self.respond(page_layout(content, "Result"))

    def respond(self, html):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(html.encode())

PORT = 8082
server = HTTPServer(("0.0.0.0", PORT), AppHandler)

print("🚀 Running: http://localhost:8082")
server.serve_forever()