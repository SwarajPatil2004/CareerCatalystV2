import React, { useEffect, useState } from 'react';
import { Save, Plus, Trash2, Loader2, Link as LinkIcon, Code, UserCircle } from 'lucide-react';
import apiClient from '../api/client';
import type { StudentProfile, Skill } from '../types';

const Profile: React.FC = () => {
  const [profile, setProfile] = useState<Partial<StudentProfile>>({});
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [profRes, skillsRes] = await Promise.all([
          apiClient.get('/students/me/profile'),
          apiClient.get('/students/me/skills')
        ]);
        setProfile(profRes.data);
        setSkills(skillsRes.data);
      } catch (error) {
        console.error('Failed to fetch profile', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await apiClient.put('/students/me/profile', profile);
      // Show success toast (not implemented)
    } finally {
      setSaving(false);
    }
  };

  if (loading) return (
    <div className="h-full flex items-center justify-center">
      <Loader2 className="w-8 h-8 animate-spin text-primary-600" />
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Edit Profile</h1>
        <p className="text-gray-600">Keep your professional information up to date.</p>
      </div>

      {/* Basic Info */}
      <section className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex items-center gap-2 mb-6">
          <div className="p-2 bg-primary-50 rounded-lg">
            <UserCircle className="w-5 h-5 text-primary-600" />
          </div>
          <h2 className="text-lg font-bold text-gray-900">Basic Information</h2>
        </div>
        <form onSubmit={handleProfileSave} className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Headline</label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
              placeholder="e.g. Aspiring Software Engineer | Final Year CS Student"
              value={profile.headline || ''}
              onChange={(e) => setProfile({ ...profile, headline: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Branch</label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
              value={profile.branch || ''}
              onChange={(e) => setProfile({ ...profile, branch: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Year of Study</label>
            <input
              type="number"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
              value={profile.current_year || ''}
              onChange={(e) => setProfile({ ...profile, current_year: parseInt(e.target.value) })}
            />
          </div>
          <div className="md:col-span-2 flex justify-end">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 flex items-center gap-2 disabled:opacity-50"
            >
              {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              Save Changes
            </button>
          </div>
        </form>
      </section>

      {/* Skills Section (Simplified for now) */}
      <section className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-blue-50 rounded-lg">
              <Code className="w-5 h-5 text-blue-600" />
            </div>
            <h2 className="text-lg font-bold text-gray-900">Skills</h2>
          </div>
          <button className="text-primary-600 flex items-center gap-1 font-semibold text-sm hover:underline">
            <Plus className="w-4 h-4" /> Add Skill
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {skills.map((skill) => (
            <div key={skill.id} className="px-3 py-1 bg-gray-50 border border-gray-200 rounded-full flex items-center gap-2 group">
              <span className="text-sm font-medium text-gray-700">{skill.name}</span>
              <button className="text-gray-400 hover:text-red-500">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))}
          {skills.length === 0 && <p className="text-gray-500 text-sm italic">No skills added yet.</p>}
        </div>
      </section>
      
      {/* Links */}
      <section className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex items-center gap-2 mb-6">
          <div className="p-2 bg-purple-50 rounded-lg">
            <LinkIcon className="w-5 h-5 text-purple-600" />
          </div>
          <h2 className="text-lg font-bold text-gray-900">Links & Portfolio</h2>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">GitHub URL</label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
              value={profile.github_link || ''}
              onChange={(e) => setProfile({ ...profile, github_link: e.target.value })}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn URL</label>
            <input
              type="text"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"
              value={profile.linkedin_link || ''}
              onChange={(e) => setProfile({ ...profile, linkedin_link: e.target.value })}
            />
          </div>
        </div>
      </section>
    </div>
  );
};

export default Profile;
