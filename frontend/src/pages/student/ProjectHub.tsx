import React, { useState, useEffect } from 'react';
import { 
  Send, Layers, Shield, 
  Search, CheckCircle2, 
  ExternalLink, MessageSquare,
  AlertCircle, ChevronRight, Play
} from 'lucide-react';
import axios from 'axios';

const ProjectHub = () => {
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [queue, setQueue] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<'my_work' | 'review_queue'>('my_work');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [subRes, qRes] = await Promise.all([
          axios.get('/api/p2p/my-submissions', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}),
          axios.get('/api/p2p/queue', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }})
        ]);
        setSubmissions(subRes.data);
        setQueue(qRes.data);
      } catch (error) {
        console.error('Error fetching P2P data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="max-w-6xl mx-auto p-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Project HUB</h1>
          <p className="text-gray-500 mt-2 text-lg">P2P Project Reviews & Skill Validation</p>
        </div>
        
        <div className="flex bg-gray-100 p-1.5 rounded-2xl border border-gray-200">
          <button 
            onClick={() => setActiveTab('my_work')}
            className={`px-6 py-2.5 rounded-xl font-bold transition-all flex items-center gap-2 ${activeTab === 'my_work' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <Layers size={18} /> My Work
          </button>
          <button 
            onClick={() => setActiveTab('review_queue')}
            className={`px-6 py-2.5 rounded-xl font-bold transition-all flex items-center gap-2 ${activeTab === 'review_queue' ? 'bg-white text-indigo-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}
          >
            <Shield size={18} /> Review Queue
            <span className="bg-indigo-600 text-white text-[10px] px-1.5 py-0.5 rounded-full ml-1">NEW</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
           {activeTab === 'my_work' ? (
             <div className="space-y-6">
                <div className="bg-white rounded-3xl p-8 border border-dashed border-gray-300 flex flex-col items-center justify-center text-center group hover:border-indigo-400 hover:bg-indigo-50/20 transition-all cursor-pointer">
                   <div className="w-16 h-16 bg-gray-50 text-gray-400 flex items-center justify-center rounded-2xl mb-4 group-hover:bg-indigo-600 group-hover:text-white transition-all shadow-sm">
                      <Send size={24} />
                   </div>
                   <h3 className="text-lg font-bold text-gray-900">Submit New Project</h3>
                   <p className="text-gray-500 text-sm max-w-xs mt-2 italic">Your project must be hosted on GitHub/Vercel and have a clear README.</p>
                </div>

                <div className="space-y-4">
                  <h3 className="text-sm font-bold text-gray-400 uppercase tracking-widest pl-1">Recent Submissions</h3>
                  {submissions.map((s, i) => (
                    <div key={i} className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm flex items-center justify-between hover:shadow-md transition-shadow">
                       <div className="flex items-center gap-4">
                          <div className={`p-4 rounded-2xl ${s.status === 'approved' ? 'bg-green-50 text-green-600' : 'bg-amber-50 text-amber-600'}`}>
                             <CheckCircle2 size={24} />
                          </div>
                          <div>
                             <h4 className="font-bold text-gray-900">{s.title}</h4>
                             <p className="text-xs text-gray-400 font-mono italic">Submitted {new Date(s.timestamp).toLocaleDateString()}</p>
                          </div>
                       </div>
                       <div className="flex items-center gap-3">
                          <span className={`px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-widest ${s.status === 'approved' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                             {s.status}
                          </span>
                          <button className="p-3 bg-gray-50 text-gray-400 rounded-xl hover:text-indigo-600 hover:bg-indigo-50 transition-all">
                             <ChevronRight size={18} />
                          </button>
                       </div>
                    </div>
                  ))}
                </div>
             </div>
           ) : (
             <div className="space-y-6">
                <div className="bg-amber-50 border border-amber-200 rounded-3xl p-6 flex items-start gap-4">
                   <AlertCircle className="text-amber-600 shrink-0 mt-1" />
                   <div>
                      <h4 className="font-bold text-amber-900">Review Integrity Reminder</h4>
                      <p className="text-sm text-amber-800 leading-relaxed">Your reviews are themselves reviewed by moderators. Submitting low-quality or AI-generated reviews will result in XP penalties and submission flags.</p>
                   </div>
                </div>

                <div className="space-y-4">
                  {queue.map((req, i) => (
                    <div key={i} className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm hover:border-indigo-200 transition-all group">
                       <div className="flex items-center justify-between mb-6">
                          <div className="flex items-center gap-3">
                             <div className="w-10 h-10 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600">
                                <Search size={20} />
                             </div>
                             <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">Code Review Priority {i+1}</span>
                          </div>
                          <span className="text-xs font-mono font-bold text-indigo-600">+100 XP REWARD</span>
                       </div>
                       
                       <h3 className="text-xl font-extrabold text-gray-900 mb-2 truncate group-hover:text-indigo-600 transition-colors">{req.title}</h3>
                       <p className="text-sm text-gray-500 mb-6 italic">Submitted by a Software Engineering student in your squad.</p>
                       
                       <div className="flex items-center gap-3">
                          <button className="flex-1 py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-500 shadow-lg shadow-indigo-100 transition-all flex items-center justify-center gap-2">
                             <Play size={18} /> Start Review
                          </button>
                          <button className="p-4 bg-gray-50 text-gray-400 rounded-2xl hover:bg-gray-100 transition-all">
                             <ExternalLink size={20} />
                          </button>
                       </div>
                    </div>
                  ))}
                </div>
             </div>
           )}
        </div>

        <div className="space-y-6">
           <div className="bg-gray-900 rounded-3xl p-8 text-white relative overflow-hidden">
              <MessageSquare size={100} className="absolute -bottom-8 -right-8 opacity-10 rotate-12" />
              <h3 className="text-xl font-bold mb-4">Review Rubric</h3>
              <ul className="space-y-4">
                 {[
                   { name: "Code Quality", desc: "Naming, Cleanliness, Modularize" },
                   { name: "Architecture", desc: "Pats, State Mgmt, Scaling" },
                   { name: "Documentation", desc: "README, Comments, API Docs" },
                   { name: "Testing", desc: "Unit, Integ, Error Handling" },
                   { name: "UI/UX", desc: "Layout, Responsive, Visuals" }
                 ].map((r, i) => (
                   <li key={i} className="flex gap-3">
                      <div className="w-6 h-6 rounded-full bg-indigo-500 flex items-center justify-center text-[10px] font-bold shrink-0">
                         {i+1}
                      </div>
                      <div>
                         <p className="text-sm font-bold">{r.name}</p>
                         <p className="text-[10px] text-gray-400 uppercase tracking-tighter">{r.desc}</p>
                      </div>
                   </li>
                 ))}
              </ul>
           </div>

           <div className="bg-white rounded-3xl p-8 border border-gray-100 shadow-sm">
              <h3 className="text-lg font-bold text-gray-900 mb-2">XP Progress</h3>
              <p className="text-xs text-gray-500 mb-6 font-medium italic">Complete 2 more reviews to reach Level 12</p>
              
              <div className="space-y-6">
                 <div>
                    <div className="flex justify-between text-[10px] font-bold uppercase mb-2 text-indigo-600 tracking-widest">
                       <span>Review Master Rank</span>
                       <span>840 / 1200</span>
                    </div>
                    <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                       <div className="h-full bg-indigo-600 rounded-full" style={{width: '70%'}} />
                    </div>
                 </div>
                 
                 <div className="pt-4 border-t border-gray-50 flex items-center justify-between">
                    <span className="text-xs font-bold text-gray-400 uppercase tracking-tighter">Total Review Karma</span>
                    <span className="text-sm font-black text-indigo-600">3,420</span>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectHub;
