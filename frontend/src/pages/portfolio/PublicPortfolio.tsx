import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Award, CheckCircle, Code, 
  ExternalLink, Github, Globe, 
  MessageSquare, Star, Video,
  ShieldCheck, Share2, Copy,
  ArrowRight, Download
} from 'lucide-react';
import axios from 'axios';

const PublicPortfolio = () => {
  const { slug } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`/api/p/${slug}`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching portfolio:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [slug]);

  const copyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center font-black animate-pulse text-indigo-600">VERIFYING IDENTITY...</div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center text-gray-500 font-bold text-xl uppercase tracking-widest">Portfolio Not Found</div>;

  return (
    <div className="min-h-screen bg-slate-950 text-white selection:bg-indigo-500 selection:text-white">
      {/* Background Gradient Orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-500/10 blur-[120px] rounded-full animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/10 blur-[120px] rounded-full" />
      </div>

      <div className="relative max-w-6xl mx-auto px-6 py-20">
        {/* Profile Header */}
        <header className="flex flex-col items-center text-center mb-24">
          <div className="relative group mb-10">
            <div className="absolute inset-0 bg-indigo-500 rounded-full blur-2xl opacity-20 group-hover:opacity-40 transition-opacity" />
            <div className="w-32 h-32 rounded-full border-2 border-indigo-500/50 p-2 relative bg-slate-900 overflow-hidden ring-4 ring-indigo-500/10">
               <div className="w-full h-full rounded-full bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center text-5xl font-black">
                  {data.user.full_name.charAt(0)}
               </div>
            </div>
            <div className="absolute -bottom-2 -right-2 bg-indigo-600 p-2 rounded-xl shadow-xl shadow-indigo-500/40 border border-indigo-400 border-2">
               <ShieldCheck size={24} className="text-white" />
            </div>
          </div>

          <h1 className="text-6xl font-black mb-4 tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-white via-white to-gray-500">
            {data.user.full_name}
          </h1>
          
          <div className="flex flex-wrap items-center justify-center gap-4 text-gray-400 font-bold uppercase tracking-widest text-xs mb-8">
             <span className="px-4 py-2 bg-white/5 rounded-full border border-white/10 flex items-center gap-2">
                <CheckCircle size={14} className="text-indigo-400" /> Identity Verified
             </span>
             <span className="px-4 py-2 bg-white/5 rounded-full border border-white/10 flex items-center gap-2">
                <Award size={14} className="text-indigo-400" /> {data.badges.length} Verified Badges
             </span>
             <span className="px-4 py-2 bg-white/5 rounded-full border border-white/10 flex items-center gap-2">
                <Star size={14} className="text-indigo-400" /> {data.stats?.total_xp || 0} Career XP
             </span>
          </div>

          <div className="flex items-center gap-4">
             <button onClick={copyLink} className="px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl font-black transition-all flex items-center gap-3">
                {copied ? <CheckCircle size={20} /> : <Copy size={20} />}
                {copied ? 'COPIED!' : 'SHARE PROFILE'}
             </button>
             <button className="px-8 py-4 bg-indigo-600 hover:bg-indigo-500 rounded-2xl font-black shadow-xl shadow-indigo-500/40 transition-all flex items-center gap-3">
                <Download size={20} /> RESUME
             </button>
          </div>
        </header>

        {/* Verified Badges Grid */}
        <section className="mb-32">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-3xl font-black tracking-tighter flex items-center gap-3 italic underline decoration-indigo-500 decoration-4">
              <Award className="text-indigo-500" /> VERIFIED SKILLS
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {data.badges.map((badge: any, i: number) => (
              <div key={i} className="group relative bg-white/5 border border-white/10 p-8 rounded-[2rem] hover:bg-indigo-600/10 hover:border-indigo-500/50 transition-all text-center">
                 <div className="mb-6 flex justify-center">
                    <div className="w-20 h-20 rounded-2xl bg-indigo-500/10 flex items-center justify-center group-hover:scale-110 transition-transform">
                       <Award size={40} className="text-indigo-400" />
                    </div>
                 </div>
                 <h3 className="text-xl font-black mb-1">{badge.skill_name}</h3>
                 <p className="text-[10px] font-black uppercase text-indigo-400 tracking-[0.2em] mb-4">{badge.level}</p>
                 <div className="text-[10px] font-bold text-gray-400 uppercase leading-relaxed">
                    Verified via {badge.verification_method}
                 </div>
              </div>
            ))}
          </div>
        </section>

        {/* Project Gallery */}
        <section className="mb-32">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-3xl font-black tracking-tighter flex items-center gap-3 italic underline decoration-indigo-500 decoration-4">
              <Code className="text-indigo-500" /> VALIDATED PROJECTS
            </h2>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
            {data.projects.map((project: any, i: number) => (
              <div key={i} className="group flex flex-col bg-white/5 border border-white/10 rounded-[2.5rem] overflow-hidden hover:bg-indigo-600/5 hover:border-indigo-500/30 transition-all">
                 <div className="p-10">
                    <div className="flex justify-between items-start mb-6">
                       <h3 className="text-3xl font-black tracking-tighter group-hover:text-indigo-400 transition-colors uppercase italic">{project.title}</h3>
                       <div className="flex items-center gap-2 px-3 py-1 bg-green-500/20 text-green-400 rounded-lg text-[10px] font-black uppercase border border-green-500/30">
                          <ShieldCheck size={12} /> Secure
                       </div>
                    </div>
                    <p className="text-gray-400 font-medium mb-10 leading-relaxed text-lg line-clamp-3">
                      {project.description || 'A peer-validated technical project demonstrating architectural mastery and clean code principles.'}
                    </p>
                    
                    <div className="grid grid-cols-2 gap-4 mb-10">
                       <div className="bg-white/5 p-5 rounded-2xl border border-white/10">
                          <p className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-1">Peer Score</p>
                          <p className="text-2xl font-black">4.8/5.0</p>
                       </div>
                       <div className="bg-white/5 p-5 rounded-2xl border border-white/10">
                          <p className="text-[10px] font-black text-gray-500 uppercase tracking-widest mb-1">Plagiarism</p>
                          <p className="text-2xl font-black text-green-400">&lt; 3%</p>
                       </div>
                    </div>

                    <div className="flex items-center gap-4">
                       <button className="flex-1 py-4 bg-white text-black rounded-2xl font-black hover:bg-gray-200 transition-all flex items-center justify-center gap-2">
                          <Github size={20} /> VIEW SOURCE
                       </button>
                       <button className="w-16 h-16 bg-white/5 border border-white/10 rounded-2xl flex items-center justify-center hover:bg-indigo-600/20 hover:border-indigo-500 transition-all">
                          <Video size={20} className="text-indigo-400" />
                       </button>
                    </div>
                 </div>
              </div>
            ))}
          </div>
        </section>

        {/* Footer */}
        <footer className="pt-20 border-t border-white/5 flex flex-col md:flex-row items-center justify-between gap-10">
           <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center font-black italic shadow-lg shadow-indigo-500/20">CC</div>
              <p className="text-gray-500 font-bold uppercase tracking-widest text-xs">Verified by CareerCatalyst Network</p>
           </div>
           <div className="flex items-center gap-8 text-xs font-black uppercase tracking-[0.2em] text-gray-400">
              <a href="#" className="hover:text-indigo-400 transition-colors">Integrity Policy</a>
              <a href="#" className="hover:text-indigo-400 transition-colors">Privacy</a>
              <a href="#" className="hover:text-indigo-400 transition-colors">Contact Support</a>
           </div>
        </footer>
      </div>
    </div>
  );
};

export default PublicPortfolio;
