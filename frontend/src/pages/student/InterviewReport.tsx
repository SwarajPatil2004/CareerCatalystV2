import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  Trophy, Star, Target, 
  Lightbulb, AlertTriangle, 
  ChevronRight, Award 
} from 'lucide-react';
import axios from 'axios';

const InterviewReport = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const finalizeAndFetch = async () => {
      try {
        // First finalize to trigger scoring
        await axios.post(`/api/interviews/${sessionId}/finalize`, {}, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        
        const response = await axios.get(`/api/interviews/${sessionId}/report`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setData(response.data);
      } catch (error) {
        console.error('Error fetching report:', error);
      } finally {
        setLoading(false);
      }
    };
    finalizeAndFetch();
  }, [sessionId]);

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-500 font-medium">AI is generating your score report...</p>
      </div>
    </div>
  );

  if (!data) return <div className="p-8 text-center text-red-500">Failed to load report.</div>;

  return (
    <div className="max-w-5xl mx-auto p-8 py-12">
      <div className="flex items-center justify-between mb-12">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">Interview Breakdown</h1>
          <p className="text-gray-500 mt-2 text-lg">Detailed analysis of your {data.track.replace('_', ' ')} performance</p>
        </div>
        <div className="bg-indigo-600 text-white p-6 rounded-3xl shadow-xl shadow-indigo-200">
           <div className="flex items-center gap-2 mb-1 opacity-80">
             <Award size={18} />
             <span className="text-xs font-bold uppercase tracking-widest">Total Score</span>
           </div>
           <div className="text-5xl font-black">{Math.round(data.score)}%</div>
        </div>
      </div>

      {/* Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <div className="p-3 bg-blue-50 text-blue-600 rounded-xl w-fit mb-4">
            <Target size={24} />
          </div>
          <h3 className="font-bold text-gray-900 mb-1">XP Earned</h3>
          <p className="text-3xl font-black text-blue-600">+{Math.round(data.score * 0.5)} XP</p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <div className="p-3 bg-green-50 text-green-600 rounded-xl w-fit mb-4">
            <Star size={24} />
          </div>
          <h3 className="font-bold text-gray-900 mb-1">Communications</h3>
          <p className="text-3xl font-black text-green-600">8.4/10</p>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
          <div className="p-3 bg-amber-50 text-amber-600 rounded-xl w-fit mb-4">
            <Lightbulb size={24} />
          </div>
          <h3 className="font-bold text-gray-900 mb-1">Key Strength</h3>
          <p className="text-gray-600 text-sm">System Design & Scalability Concepts</p>
        </div>
      </div>

      {/* Detailed Question Review */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Question-by-Question Analysis</h2>
      <div className="space-y-6">
        {data.results.map((result: any, idx: number) => (
          <div key={idx} className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
            <div className="p-6 border-b border-gray-100">
               <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full uppercase tracking-widest">
                    {result.type}
                  </span>
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map(s => (
                      <Star key={s} size={14} className={s <= (result.evaluation?.score * 5) ? "fill-amber-400 text-amber-400" : "text-gray-200"} />
                    ))}
                  </div>
               </div>
               <h4 className="text-lg font-bold text-gray-900 mb-4">{result.question}</h4>
               
               <div className="bg-gray-50 p-4 rounded-xl border border-gray-100 mb-4">
                  <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Your Answer</p>
                  <p className="text-gray-700 italic leading-relaxed">
                    "{result.transcript || "No response recorded."}"
                  </p>
               </div>

               <div className="flex items-start gap-4">
                  <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg shrink-0 mt-1">
                    <Lightbulb size={20} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-gray-900 mb-1">AI Feedback</p>
                    <p className="text-sm text-gray-600 leading-relaxed">
                      {result.evaluation?.feedback || "Evaluation pending depth analysis."}
                    </p>
                  </div>
               </div>
            </div>
            {idx === 0 && (
              <div className="bg-amber-50/50 p-4 px-6 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <AlertTriangle className="text-amber-600" size={18} />
                  <span className="text-sm text-amber-800 font-medium">Critical Tip: You missed mentioning 'Normalization' in this answer.</span>
                </div>
                <button className="text-amber-900 text-xs font-bold hover:underline">View suggestion</button>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-12 flex justify-center gap-4">
          <Link to="/roadmaps" className="px-8 py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-500 shadow-xl shadow-indigo-100 transition-all flex items-center gap-2">
            Continue Learning Path <ChevronRight size={20} />
          </Link>
          <Link to="/" className="px-8 py-4 bg-white text-gray-900 border border-gray-200 rounded-2xl font-bold hover:bg-gray-50 transition-all">
            Back to Dashboard
          </Link>
      </div>
    </div>
  );
};

export default InterviewReport;
