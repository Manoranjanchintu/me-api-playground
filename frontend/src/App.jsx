import { useState, useEffect } from 'react';
import api from './api';

function App() {
    const [profile, setProfile] = useState(null);
    const [projects, setProjects] = useState([]);
    const [skills, setSkills] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState(null);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [profileRes, projectsRes, skillsRes] = await Promise.all([
                api.get('/profile'),
                api.get('/projects'),
                api.get('/skills')
            ]);
            setProfile(profileRes.data);
            setProjects(projectsRes.data);
            setSkills(skillsRes.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!searchQuery) {
            setSearchResults(null);
            return;
        }
        try {
            const res = await api.get(`/search?q=${searchQuery}`);
            setSearchResults(res.data);
        } catch (error) {
            console.error("Search error:", error);
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white font-sans p-8">
            <div className="max-w-4xl mx-auto space-y-8">

                {/* Header / Profile Section */}
                {profile && (
                    <header className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                            {profile.name}
                        </h1>
                        <p className="text-gray-400 mt-2">{profile.email}</p>
                        <div className="mt-4 flex flex-wrap gap-4">
                            {profile.work_links && Object.entries(JSON.parse(profile.work_links)).map(([key, url]) => (
                                <a key={key} href={url} target="_blank" rel="noreferrer"
                                    className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-full text-sm font-medium transition-colors capitalize">
                                    {key}
                                </a>
                            ))}
                        </div>
                        <p className="mt-4 text-gray-300 border-l-4 border-blue-500 pl-4">
                            {profile.education}
                        </p>
                    </header>
                )}

                {/* Search Section */}
                <section className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
                    <h2 className="text-2xl font-semibold mb-4 text-blue-300">API Playground Search</h2>
                    <form onSubmit={handleSearch} className="flex gap-4">
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Search projects or skills (e.g. 'python')"
                            className="flex-1 px-4 py-2 rounded bg-gray-900 border border-gray-600 focus:border-blue-500 focus:outline-none"
                        />
                        <button type="submit" className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded font-bold transition-colors">
                            Search
                        </button>
                    </form>

                    {searchResults && (
                        <div className="mt-6 space-y-4">
                            <h3 className="text-xl font-medium">Results:</h3>
                            {searchResults.projects.length === 0 && searchResults.skills.length === 0 && <p className="text-gray-500">No results found.</p>}

                            {searchResults.skills.length > 0 && (
                                <div className="flex flex-wrap gap-2 mb-4">
                                    {searchResults.skills.map(s => (
                                        <span key={s.id} className="px-3 py-1 bg-green-900 text-green-200 rounded text-sm border border-green-700">
                                            {s.name}
                                        </span>
                                    ))}
                                </div>
                            )}

                            {searchResults.projects.map(p => (
                                <div key={p.id} className="p-4 bg-gray-700 rounded border-l-4 border-yellow-500">
                                    <h4 className="font-bold">{p.title}</h4>
                                    <p className="text-sm text-gray-300">{p.description}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </section>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Skills Section */}
                    <section>
                        <h2 className="text-2xl font-bold mb-4 text-purple-400">Skills</h2>
                        <div className="flex flex-wrap gap-3">
                            {skills.map(skill => (
                                <div key={skill.id} className={`px-4 py-2 rounded-lg border ${skill.is_top ? 'bg-purple-900 border-purple-500' : 'bg-gray-800 border-gray-700'}`}>
                                    <span className="font-bold">{skill.name}</span>
                                    {skill.proficiency && <span className="text-xs ml-2 text-gray-400">({skill.proficiency})</span>}
                                </div>
                            ))}
                        </div>
                    </section>

                    {/* Projects Section */}
                    <section>
                        <h2 className="text-2xl font-bold mb-4 text-green-400">Projects</h2>
                        <div className="space-y-4">
                            {projects.map(project => (
                                <div key={project.id} className="bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-green-500 transition-colors">
                                    <h3 className="text-xl font-bold">{project.title}</h3>
                                    <p className="text-gray-400 text-sm mt-1">{project.description}</p>
                                    <div className="mt-3 flex gap-2">
                                        {project.links && Object.entries(JSON.parse(project.links)).map(([key, url]) => (
                                            <a key={key} href={url} className="text-blue-400 hover:text-blue-300 text-xs uppercase font-bold tracking-wider">
                                                {key} &rarr;
                                            </a>
                                        ))}
                                    </div>
                                    <div className="mt-3 pt-3 border-t border-gray-700 flex flex-wrap gap-2">
                                        {project.skills.map(s => (
                                            <span key={s.id} className="text-xs px-2 py-0.5 bg-gray-900 text-gray-400 rounded-full">
                                                {s.name}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </section>
                </div>

            </div>
        </div>
    )
}

export default App
