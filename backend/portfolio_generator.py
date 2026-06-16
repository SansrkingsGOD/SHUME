def generate_portfolio_html(data: dict) -> str:
    p = data.get("personal", {})
    name = p.get("name", "Your Name")
    role = data.get("summary", "Software Engineer")[:60]
    email = p.get("email","")
    github = p.get("github","")
    linkedin = p.get("linkedin","")

    skills_all = []
    for v in data.get("skills",{}).values():
        if isinstance(v, list): skills_all.extend(v)
        else: skills_all.append(v)

    skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in skills_all[:20])

    projects_html = ""
    for proj in data.get("projects",[]):
        projects_html += f"""
        <div class="project-card">
          <h3>{proj.get('name','')}</h3>
          <p class="tech-stack">{proj.get('tech','')}</p>
          <p>{proj.get('description','')}</p>
          {'<a href="'+proj["link"]+'" target="_blank">View Project →</a>' if proj.get("link") else ""}
        </div>"""

    exp_html = ""
    for exp in data.get("experience",[]):
        bullets = "".join(f"<li>{b}</li>" for b in exp.get("bullets",[]) if b.strip())
        exp_html += f"""
        <div class="exp-item">
          <div class="exp-header">
            <div><h3>{exp.get('title','')}</h3><p>{exp.get('company','')} &mdash; {exp.get('location','')}</p></div>
            <span class="duration">{exp.get('duration','')}</span>
          </div>
          <ul>{bullets}</ul>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — Portfolio</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#1a2e4a;--blue:#2563eb;--light:#f8fafc;--gray:#64748b;--border:#e2e8f0}}
body{{font-family:'DM Sans',sans-serif;background:#fff;color:#0f172a;line-height:1.6}}
nav{{position:fixed;top:0;width:100%;background:rgba(255,255,255,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center;z-index:100}}
nav .logo{{font-family:'DM Serif Display',serif;font-size:1.2rem;color:var(--navy)}}
nav ul{{list-style:none;display:flex;gap:2rem}}
nav a{{text-decoration:none;color:var(--gray);font-size:.9rem;transition:.2s}}
nav a:hover{{color:var(--blue)}}
.hero{{min-height:100vh;display:flex;align-items:center;padding:6rem 2rem 4rem;max-width:1100px;margin:auto}}
.hero-text h1{{font-family:'DM Serif Display',serif;font-size:3.5rem;color:var(--navy);line-height:1.1;margin-bottom:1rem}}
.hero-text h1 span{{color:var(--blue)}}
.hero-text p{{font-size:1.1rem;color:var(--gray);max-width:520px;margin-bottom:2rem}}
.btn{{display:inline-flex;align-items:center;gap:.5rem;padding:.8rem 1.8rem;background:var(--blue);color:#fff;border-radius:8px;text-decoration:none;font-weight:500;transition:.2s;margin-right:1rem}}
.btn:hover{{background:#1d4ed8}}
.btn.outline{{background:transparent;border:1.5px solid var(--navy);color:var(--navy)}}
.btn.outline:hover{{background:var(--navy);color:#fff}}
section{{padding:5rem 2rem;max-width:1100px;margin:auto}}
h2.sec-title{{font-family:'DM Serif Display',serif;font-size:2rem;color:var(--navy);margin-bottom:.4rem}}
.sec-line{{width:48px;height:3px;background:var(--blue);margin-bottom:2.5rem;border-radius:2px}}
.skills-grid{{display:flex;flex-wrap:wrap;gap:.6rem}}
.skill-tag{{padding:.35rem .9rem;background:var(--light);border:1px solid var(--border);border-radius:20px;font-size:.85rem;color:var(--navy);font-weight:500}}
.projects-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:1.5rem}}
.project-card{{padding:1.8rem;border:1px solid var(--border);border-radius:12px;transition:.2s}}
.project-card:hover{{box-shadow:0 8px 30px rgba(37,99,235,.1);border-color:var(--blue);transform:translateY(-2px)}}
.project-card h3{{color:var(--navy);margin-bottom:.4rem;font-size:1.05rem}}
.project-card .tech-stack{{font-size:.8rem;color:var(--blue);margin-bottom:.6rem;font-weight:500}}
.project-card p{{color:var(--gray);font-size:.9rem;margin-bottom:.8rem}}
.project-card a{{color:var(--blue);text-decoration:none;font-size:.9rem;font-weight:500}}
.exp-item{{margin-bottom:2rem;padding-bottom:2rem;border-bottom:1px solid var(--border)}}
.exp-item:last-child{{border-bottom:none}}
.exp-header{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.5rem}}
.exp-header h3{{color:var(--navy);font-size:1rem}}
.exp-header p{{color:var(--gray);font-size:.85rem}}
.duration{{background:var(--light);padding:.2rem .8rem;border-radius:20px;font-size:.8rem;color:var(--gray);white-space:nowrap}}
.exp-item ul{{padding-left:1.2rem;color:var(--gray);font-size:.9rem}}
.exp-item li{{margin-bottom:.3rem}}
.contact-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem}}
.contact-card{{text-align:center;padding:1.5rem;border:1px solid var(--border);border-radius:12px}}
.contact-card a{{color:var(--blue);text-decoration:none;font-weight:500}}
footer{{text-align:center;padding:2rem;color:var(--gray);font-size:.85rem;border-top:1px solid var(--border)}}
@media(max-width:600px){{.hero-text h1{{font-size:2.2rem}}.exp-header{{flex-direction:column;gap:.4rem}}}}
</style>
</head>
<body>
<nav>
  <span class="logo">{name.split()[0]}</span>
  <ul>
    <li><a href="#skills">Skills</a></li>
    <li><a href="#projects">Projects</a></li>
    <li><a href="#experience">Experience</a></li>
    <li><a href="#contact">Contact</a></li>
  </ul>
</nav>

<div class="hero">
  <div class="hero-text">
    <h1>Hi, I'm <span>{name.split()[0]}</span>.<br>{name.split()[-1] if len(name.split())>1 else ''}</h1>
    <p>{role}</p>
    <a href="#projects" class="btn">View Projects</a>
    <a href="#contact" class="btn outline">Get In Touch</a>
  </div>
</div>

<section id="skills">
  <h2 class="sec-title">Skills</h2>
  <div class="sec-line"></div>
  <div class="skills-grid">{skills_html}</div>
</section>

<section id="projects">
  <h2 class="sec-title">Projects</h2>
  <div class="sec-line"></div>
  <div class="projects-grid">{projects_html}</div>
</section>

<section id="experience">
  <h2 class="sec-title">Experience</h2>
  <div class="sec-line"></div>
  {exp_html}
</section>

<section id="contact">
  <h2 class="sec-title">Get In Touch</h2>
  <div class="sec-line"></div>
  <div class="contact-grid">
    {'<div class="contact-card"><p>Email</p><a href="mailto:'+email+'">'+email+'</a></div>' if email else ''}
    {'<div class="contact-card"><p>GitHub</p><a href="'+github+'" target="_blank">'+github+'</a></div>' if github else ''}
    {'<div class="contact-card"><p>LinkedIn</p><a href="'+linkedin+'" target="_blank">LinkedIn Profile</a></div>' if linkedin else ''}
  </div>
</section>

<footer><p>Built with AI Resume & Portfolio Builder &mdash; {name}</p></footer>
</body></html>"""
