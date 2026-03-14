import React, { useState, useEffect } from 'react';
import { 
  Search, Filter, Briefcase, 
  MapPin, GraduationCap, Award,
  CheckCircle, Star, Download,
  Mail, ExternalLink, ChevronRight
} from 'lucide-react';
import axios from 'axios';

const RecruiterDashboard = () => {
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    skills: '',
    minXp: 0,
    role: 'All Roles'
  });

  useEffect(() => {
    const fetchCandidates = async () => {
      setLoading(true);
      try {
        const response = await axios.get(`/api/recruiter/search`);
        setCandidates(response.data);
      } catch (error) {
        console.error('Error fetching candidates:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchCandidates();
  }, [filters]);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar Filters */}
      <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto p-8 hidden lg:block">
        <div className="flex items-center gap-3 mb-10">
          <div className="bg-indigo-600 p-2 rounded-xl text-white">
            <Briefcase size={20} />
          </div>
          <h2 className="text-xl font-bold text-gray-900 tracking-tight">Recruiter Hub</h2>
        </div>

        <div className="space-y-8">
          <div>
            <label className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4 block">Candidate Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={18} />
              <input 
                type="text" 
                placeholder="Search skills, names..." 
                className="w-full pl-10 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-2xl text-sm focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all outline-none"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4 block">Experience (XP)</label>
            <input 
              type="range" 
              min="0" 
              max="10000" 
              step="500"
              className="w-full h-1.5 bg-gray-100 rounded-full appearance-none cursor-pointer accent-indigo-600"
            />
            <div className="flex justify-between text-[10px] font-bold text-gray-400 mt-2">
              <span>0 XP</span>
              <span>10K+ XP</span>
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4 block">Target Role</label>
            <div className="space-y-2">
              {['Frontend Developer', 'Backend Developer', 'Data Scientist', 'AI Engineer'].map((role) => (
                <label key={role} className="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 cursor-pointer group transition-all">
                  <input type="checkbox" className="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
                  <span className="text-sm font-medium text-gray-600 group-hover:text-gray-900">{role}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="pt-8 mt-8 border-t border-gray-100">
             <button className="w-full py-4 bg-gray-900 text-white rounded-2xl font-bold hover:bg-gray-800 transition-all flex items-center justify-center gap-2 shadow-lg shadow-gray-200">
                <Download size={18} /> Export Shortlist (CSV)
             </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-8 lg:p-12">
          <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
            <div>
              <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Discover Talent</h1>
              <p className="text-gray-500 mt-2 text-lg">Verified candidate profiles from top institutions</p>
            </div>
            
            <div className="flex items-center gap-4 bg-white p-2 rounded-2xl border border-gray-100 shadow-sm">
               <div className="px-4 py-2 bg-indigo-50 text-indigo-600 rounded-xl text-sm font-bold border border-indigo-100 flex items-center gap-2">
                  <Award size={16} /> Verified Only
               </div>
               <div className="h-4 w-px bg-gray-100 mx-2" />
               <span className="text-xs font-bold text-gray-400 uppercase px-4 truncate">California Tech Hub 2026 Batch</span>
            </div>
          </header>

          {loading ? (
            <div className="p-20 text-center text-gray-400 italic">Searching verified talent...</div>
          ) : (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
              {candidates.map((c, i) => (
                <div key={i} className="bg-white rounded-[2rem] border border-gray-100 p-8 shadow-sm hover:shadow-xl hover:shadow-indigo-50/50 hover:border-indigo-100 transition-all group relative overflow-hidden">
                   <div className="absolute top-0 right-0 p-8">
                      <div className="bg-green-50 text-green-600 text-[10px] font-bold px-3 py-1 rounded-full border border-green-100 flex items-center gap-1 uppercase tracking-widest animate-pulse">
                        <CheckCircle size={12} /> Verified
                      </div>
                   </div>

                   <div className="flex items-start gap-6 mb-8">
                      <div className="w-20 h-20 rounded-3xl bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold text-2xl border-4 border-white shadow-md">
                         {c.full_name?.charAt(0) || 'S'}
                      </div>
                      <div>
                         <h3 className="text-2xl font-black text-gray-900 mb-1 group-hover:text-indigo-600 transition-colors">{c.full_name || 'Anonymous Talent'}</h3>
                         <div className="flex items-center gap-4 text-xs font-bold text-gray-400">
                            <span className="flex items-center gap-1"><MapPin size={12} /> New York, NY</span>
                            <span className="flex items-center gap-1"><GraduationCap size={12} /> Class of 2026</span>
                         </div>
                      </div>
                   </div>

                   <div className="grid grid-cols-3 gap-4 mb-8">
                      <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 group-hover:bg-indigo-50/30 group-hover:border-indigo-100 transition-all">
                         <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Interview Score</p>
                         <p className="text-lg font-black text-gray-900">8.4/10</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 group-hover:bg-indigo-50/30 group-hover:border-indigo-100 transition-all">
                         <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Total XP</p>
                         <p className="text-lg font-black text-gray-900">1.2K</p>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-2xl border border-gray-100 group-hover:bg-indigo-50/30 group-hover:border-indigo-100 transition-all">
                         <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Projects Done</p>
                         <p className="text-lg font-black text-gray-900">12</p>
                      </div>
                   </div>

                   <div className="flex flex-wrap gap-2 mb-8">
                      {['React', 'TypeScript', 'Node.js', 'PostgreSQL', 'Docker'].map(skill => (
                        <span key={skill} className="px-3 py-1.5 bg-gray-50 text-gray-500 rounded-lg text-[10px] font-bold group-hover:bg-indigo-100/50 group-hover:text-indigo-600 transition-all uppercase tracking-tighter">
                          {skill}
                        </span>
                      ))}
                   </div>

                   <div className="flex items-center gap-4">
                      <button className="flex-1 py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-100 flex items-center justify-center gap-2">
                         <Star size={18} /> Request Interview
                      </button>
                      <button className="p-4 bg-gray-900 text-white rounded-2xl hover:bg-gray-800 transition-all shadow-lg shadow-gray-200">
                         <ChevronRight size={18} />
                      </button>
                   </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecruiterDashboard;
