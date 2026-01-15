import { useEffect, useState } from "react";

const API_URL = "https://me-api-backend-1gn4.onrender.com";

function App() {
  const [profile, setProfile] = useState(null);
  const [projects, setProjects] = useState([]);
  const [skills, setSkills] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/profile`)
      .then(res => res.json())
      .then(data => setProfile(data));

    fetch(`${API_URL}/projects`)
      .then(res => res.json())
      .then(data => setProjects(data));

    fetch(`${API_URL}/skills`)
      .then(res => res.json())
      .then(data => setSkills(data));
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Me API Playground</h1>

      {profile && (
        <div>
          <h2>{profile.name}</h2>
          <p>{profile.email}</p>
          <p>{profile.education}</p>
        </div>
      )}

      <h3>Skills</h3>
      <ul>
        {skills.map(skill => (
          <li key={skill.id}>{skill.name} — {skill.proficiency}</li>
        ))}
      </ul>

      <h3>Projects</h3>
      <ul>
        {projects.map(project => (
          <li key={project.id}>{project.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
