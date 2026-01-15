import { useEffect, useState } from "react";
import { API_BASE_URL } from "./config";
import "./App.css";

function App() {
  const [profile, setProfile] = useState(null);
  const [projects, setProjects] = useState([]);
  const [skills, setSkills] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/profile`)
      .then(res => res.json())
      .then(setProfile);

    fetch(`${API_BASE_URL}/skills`)
      .then(res => res.json())
      .then(setSkills);

    fetch(`${API_BASE_URL}/projects`)
      .then(res => res.json())
      .then(setProjects);
  }, []);

  return (
    <div className="container">
      <h1 className="title">Me API Playground</h1>

      {profile && (
        <div className="card profile">
          <h2>{profile.name}</h2>
          <p>{profile.email}</p>
          <p>{profile.education}</p>
        </div>
      )}

      <h2 className="section-title">Skills</h2>
      <div className="grid">
        {skills.map(skill => (
          <div className="card" key={skill.id}>
            <h3>{skill.name}</h3>
            <p>{skill.proficiency}</p>
          </div>
        ))}
      </div>

      <h2 className="section-title">Projects</h2>
      <div className="grid">
        {projects.map(project => (
          <div className="card" key={project.id}>
            <h3>{project.title}</h3>
            <p>{project.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
