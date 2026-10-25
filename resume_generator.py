import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUT = os.environ.get("RESUME_OUTPUT", "output/pdf/PRADYUMNA_JK_Qualcomm_Targeted_Resume.pdf")
doc = SimpleDocTemplate(OUT, pagesize=LETTER, rightMargin=.55*inch, leftMargin=.55*inch, topMargin=.4*inch, bottomMargin=.4*inch)
s = getSampleStyleSheet(); ink=colors.HexColor("#303030"); blue=colors.HexColor("#1667d9"); grey=colors.HexColor("#555555")
s.add(ParagraphStyle("Name", parent=s["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=24, textColor=ink))
s.add(ParagraphStyle("Role", parent=s["Normal"], fontSize=10.5, leading=13, textColor=grey))
s.add(ParagraphStyle("Contact", parent=s["Normal"], fontSize=8.7, leading=12, textColor=blue, alignment=TA_RIGHT))
s.add(ParagraphStyle("Section", parent=s["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceBefore=9, spaceAfter=4, textColor=ink))
s.add(ParagraphStyle("Body", parent=s["BodyText"], fontSize=8.9, leading=11.7, textColor=ink, spaceAfter=2))
s.add(ParagraphStyle("Small", parent=s["BodyText"], fontSize=8.5, leading=11, textColor=ink))
s.add(ParagraphStyle("Job", parent=s["BodyText"], fontName="Helvetica-Bold", fontSize=9.8, leading=12, textColor=ink))
s.add(ParagraphStyle("Org", parent=s["BodyText"], fontName="Helvetica-Oblique", fontSize=8.6, leading=10.5, textColor=grey))
s.add(ParagraphStyle("Proj", parent=s["BodyText"], fontName="Helvetica-BoldOblique", fontSize=9.4, leading=11.5, spaceBefore=4, spaceAfter=1))
s.add(ParagraphStyle("ResumeBullet", parent=s["BodyText"], fontSize=8.5, leading=10.8, leftIndent=12, firstLineIndent=-8, textColor=ink, spaceAfter=1))
def p(x, st="Body"): return Paragraph(x, s[st])
def bullets(xs): return [p("• " + x, "ResumeBullet") for x in xs]
story=[]
head=Table([[p("PRADYUMNA JK","Name"),p("pradyumna.jk@gmail.com<br/>+91 9000327328<br/>Telangana, India<br/><font color='#1667d9'>linkedin.com/in/pradyumna-jk<br/>github.com/Pradyumna-JK</font>","Contact")]],colWidths=[4.4*inch,2.55*inch])
head.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
story += [head,p("Software Engineer | Full-Stack | AI/ML | Cloud-Native Systems","Role"),Spacer(1,4)]
story += [p("SUMMARY","Section"),p("Full-stack software engineer building reliable, user-focused systems across React, TypeScript, Python, FastAPI, PostgreSQL, Docker, Linux, and cloud-oriented architectures. Experienced in designing REST APIs, real-time interfaces, persistent data workflows, automated tests, and AI/ML features while collaborating across technical and business teams.","Body")]
story += [p("PROFESSIONAL EXPERIENCE & PAID CLIENT WORK","Section")]
def job(title,org,date,items):
 t=Table([[p(title,"Job"),p(date,"Small")],[p(org,"Org"),p("","Small")]],colWidths=[5.2*inch,1.75*inch]); t.setStyle(TableStyle([("ALIGN",(1,0),(1,0),"RIGHT"),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)])); return [t]+bullets(items)
story += job("Strategy & Operations Analyst (SNOW support team)","HighRadius","Aug 2025 - Present",["Built a Python ML pipeline to predict poor-CSAT support cases using class-weighted logistic regression (ROC-AUC ~0.78 across 1,174 cases).","Improved signal quality with SMOTE, SHAP explainability, and zero-shot taxonomy classification; translated model output into operational decisions.","Produced weekly business reviews across six enterprise products using support cohorts, operational KPIs, and customer-satisfaction trends."])
story += job("Full-Stack Developer","Indian Army - Employee Management System","Mar 2025 - May 2025",["Developed and deployed an employee-management system integrating an ESP32-hosted web server for local-network access without external cloud hosting.","Worked across application development, embedded networking, and on-premises infrastructure to deliver an end-to-end system."])
story += job("Fleet Management Application Developer","M&K Logistics","Aug 2024 - Aug 2025",["Engineered a Flutter/Dart/PostgreSQL fleet application for attendance, shift tracking, trip reporting, and vehicle administration across 50+ vehicles and 30+ drivers.","Implemented role-based workflows, GPS-enabled attendance, vehicle assignments, document verification, authentication, and real-time driver activity."])
story += job("SQL Server High Availability Consultant (Freelance)","Soda Bay Company - United States (Remote)","Feb 2025 - Mar 2025",["Contributed to configuring a two-node Microsoft SQL Server high-availability environment on Windows Server 2022, supporting database redundancy and failover readiness.","Configured certificate-based authentication, database-mirroring endpoints, and server-to-server connectivity for SQL Server Always On Availability Groups.","Diagnosed Windows Server Failover Clustering (WSFC), SSL authentication, firewall, DNS, and network connectivity issues to improve database availability and operational resilience.","<b>Technologies:</b> Microsoft SQL Server, Windows Server 2022, T-SQL, WSFC, Always On Availability Groups, TCP/IP, SSL certificates."])
story += job("Full-Stack Developer & Hardware Integration Lead", "Deloitte - Innoverse Smart Retail Automation Prototype", "Project engagement", ["Developed a full-stack web application for a two-floor futuristic smart-retail prototype, enabling software interaction with physical store components.","Engineered and integrated motor-driven levitation mechanisms by combining electronics, hardware controls, and application functionality.","Led backend development and hardware integration, connecting digital control interfaces with electromechanical components.","Contributed to an interdisciplinary retail-technology prototype spanning web development, embedded electronics, and automation."])
story += [p("EDUCATION","Section"),p("<b>Woxsen University, Hyderabad</b> | B.Tech, Computer Science & Engineering (AI & ML) | 2022 - 2026","Body"),p("<b>Relevant coursework:</b> Data Structures & Algorithms, Operating Systems, Computer Networks, Object-Oriented Programming","Small")]
story += [p("TECHNICAL SKILLS","Section"),p("<b>Languages:</b> Python, C++, C, JavaScript/TypeScript, SQL, Bash<br/><b>Frontend:</b> React, Vite, responsive UI, SSE<br/><b>Backend/Data:</b> FastAPI, REST APIs, SQLAlchemy, PostgreSQL, NoSQL concepts<br/><b>Cloud/DevOps:</b> AWS fundamentals, Docker, Docker Compose, GitHub Actions, Linux, Git<br/><b>AI/ML:</b> Ollama, ONNX Runtime, PyTorch/TensorFlow, scikit-learn, SHAP","Small")]
story += [p("SELECTED PROJECTS","Section")]
def project(title,stack,items): return [p(title,"Proj"),p("<b>Tech:</b> "+stack,"Small")]+bullets(items)
story += project("OpsPilot - Multi-Tenant AI Operations Hub","Python, FastAPI, React, TypeScript, PostgreSQL, SQLAlchemy, Docker, SSE, GitHub Actions",["Built a tenant-scoped operations dashboard with REST APIs, signed-cookie auth boundaries, role-aware access, encrypted OAuth-token primitives, and health checks.","Implemented a GitHub webhook ingestion path with HMAC signature validation, replay deduplication, event persistence, and tenant-filtered Server-Sent Events for live dashboard updates.","Created Docker Compose infrastructure for API, React web app, and PostgreSQL; added a clean frontend shell with demo-mode metrics and live activity feed."])
story += project("DealMind (Yureni) - Local-First AI Deal Intelligence","Python, FastAPI, React, TypeScript, PostgreSQL, Ollama, Hindsight memory, Docker",["Built an AI sales-intelligence platform that stores meetings, emails, and notes as persistent searchable deal memory.","Implemented evidence-grounded Q&A, temporal stakeholder analysis, explainable deal-risk scoring, deal/timeline/stakeholder APIs, and source traceability.","Delivered a React dashboard and voice interface with Dockerized services and backend, frontend, and AI evaluation tests; resolved a production-style memory extraction issue by separating answer and extraction models.","Selected as a finalist at the Devnovate Hackathon hosted at the Microsoft office in Hyderabad for the DealMind prototype."])
story += [p("ACHIEVEMENTS & CERTIFICATIONS","Section"),p("<b>Leadership:</b> IEEE Student Branch - Chairperson; Secretary - Baudhik Club; Co-founder - The Karm Haus Studio<br/><b>Certifications:</b> Data Structures (UC San Diego); Algorithms for Searching, Sorting and Indexing (CU Boulder); Deep Learning with Keras (IBM); AWS Cloud Foundation","Small")]
doc.build(story)
print(OUT)
