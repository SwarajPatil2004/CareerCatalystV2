import React, { useEffect, useState } from 'react';
import { 
  ChevronDown, 
  ChevronUp, 
  CheckCircle2, 
  Circle, 
  Trophy, 
  Zap,
  BookOpen
} from 'lucide-react';
import apiClient from '../api/client';
import { cn } from '../utils/cn';

interface Task {
  id: number;
  title: string;
  description: string;
  resource_link: string;
  xp: number;
}

interface Phase {
  id: number;
  phase_index: number;
  title: string;
  description: string;
  tasks: Task[];
}

interface Roadmap {
  id: number;
  name: string;
  description: string;
  phases: Phase[];
}

interface Progress {
  completed_task_ids: number[];
  total_xp: number;
}

const CareerGrind: React.FC = () => {
  const [selectedRoadmap, setSelectedRoadmap] = useState<Roadmap | null>(null);
  const [progress, setProgress] = useState<Progress>({ completed_task_ids: [], total_xp: 0 });
  const [expandedPhases, setExpandedPhases] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRoadmaps();
  }, []);

  const fetchRoadmaps = async () => {
    try {
      const res = await apiClient.get('/roadmaps');
      if (res.data.length > 0) {
        fetchRoadmapDetails(res.data[0].slug);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchRoadmapDetails = async (slug: string) => {
    try {
      const roadmapRes = await apiClient.get(`/roadmaps/${slug}`);
      const progressRes = await apiClient.get(`/roadmaps/${roadmapRes.data.id}/progress`);
      setSelectedRoadmap(roadmapRes.data);
      setProgress(progressRes.data);
      // Auto-expand first phase
      if (roadmapRes.data.phases.length > 0) {
        setExpandedPhases([roadmapRes.data.phases[0].id]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const togglePhase = (phaseId: number) => {
    setExpandedPhases(prev => 
      prev.includes(phaseId) ? prev.filter(id => id !== phaseId) : [...prev, phaseId]
    );
  };

  const toggleTask = async (taskId: number) => {
    if (progress.completed_task_ids.includes(taskId)) return;
    
    try {
      const res = await apiClient.post('/roadmaps/tasks/complete', { task_id: taskId });
      setProgress(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return (
    <div className="flex items-center justify-center min-h-[400px]">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
  );

  const totalTasks = selectedRoadmap?.phases.reduce((acc, p) => acc + p.tasks.length, 0) || 0;
  const completedCount = progress.completed_task_ids.length;
  const progressPercent = totalTasks > 0 ? (completedCount / totalTasks) * 100 : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-2">
            Career Grind
          </h1>
          <p className="text-lg text-gray-600">
            Master your path and earn XP by completing tasks.
          </p>
        </div>
        
        <div className="bg-primary-600 rounded-3xl p-6 text-white shadow-2xl shadow-primary-900/40 min-w-[200px] transform hover:scale-105 transition-transform">
          <div className="flex items-center gap-3 mb-2">
            <Zap className="w-6 h-6 text-yellow-300 fill-yellow-300" />
            <span className="text-sm font-bold uppercase tracking-widest opacity-80">Total XP</span>
          </div>
          <p className="text-4xl font-black italic">{progress.total_xp}</p>
        </div>
      </div>

      {/* Progress Card */}
      <div className="bg-white rounded-[2.5rem] p-8 shadow-sm border border-gray-100">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Trophy className="w-7 h-7 text-primary-600" />
            <h2 className="text-xl font-bold text-gray-900">Roadmap Progress</h2>
          </div>
          <span className="text-lg font-bold text-primary-600">{Math.round(progressPercent)}%</span>
        </div>
        
        <div className="h-4 bg-gray-100 rounded-full overflow-hidden shadow-inner">
          <div 
            className="h-full bg-primary-600 rounded-full transition-all duration-1000 ease-out shadow-lg"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        
        <div className="mt-4 flex justify-between text-sm font-bold text-gray-500 uppercase tracking-tighter italic">
          <span>{completedCount} Tasks Completed</span>
          <span>{totalTasks} Total Tasks</span>
        </div>
      </div>

      {/* Phases */}
      <div className="space-y-4">
        {selectedRoadmap?.phases.sort((a,b) => a.phase_index - b.phase_index).map((phase, idx) => (
          <div key={phase.id} className="group">
            <div 
              className={cn(
                "bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden transition-all duration-300",
                expandedPhases.includes(phase.id) ? "ring-2 ring-primary-600/20" : "hover:border-gray-200"
              )}
            >
              <button 
                onClick={() => togglePhase(phase.id)}
                className="w-full flex items-center justify-between p-6 text-left"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-gray-100 rounded-2xl flex items-center justify-center text-gray-600 font-black italic">
                    {idx + 1}
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900 group-hover:text-primary-600 transition-colors uppercase tracking-tight">
                      {phase.title}
                    </h3>
                    <p className="text-sm text-gray-500">{phase.tasks.length} Learning Tasks</p>
                  </div>
                </div>
                {expandedPhases.includes(phase.id) ? (
                  <ChevronUp className="w-6 h-6 text-gray-400" />
                ) : (
                  <ChevronDown className="w-6 h-6 text-gray-400" />
                )}
              </button>

              {expandedPhases.includes(phase.id) && (
                <div className="px-6 pb-6 space-y-3 animate-in fade-in slide-in-from-top-2 duration-300">
                   <div className="p-4 bg-gray-50 rounded-2xl mb-4 border-l-4 border-primary-500">
                    <p className="text-gray-600 text-sm leading-relaxed">{phase.description}</p>
                  </div>
                  {phase.tasks.map(task => {
                    const isDone = progress.completed_task_ids.includes(task.id);
                    return (
                      <div 
                        key={task.id}
                        className={cn(
                          "flex items-center gap-4 p-4 rounded-[1.5rem] border transition-all duration-200",
                          isDone 
                            ? "bg-green-50/50 border-green-100" 
                            : "bg-white border-gray-100 hover:border-primary-200 hover:shadow-md"
                        )}
                      >
                        <button 
                          onClick={() => toggleTask(task.id)}
                          className={cn(
                            "flex-shrink-0 transition-transform active:scale-90",
                            isDone ? "text-green-600" : "text-gray-300 hover:text-primary-500"
                          )}
                        >
                          {isDone ? (
                            <CheckCircle2 className="w-7 h-7 fill-green-50" />
                          ) : (
                            <Circle className="w-7 h-7" />
                          )}
                        </button>
                        
                        <div className="flex-1 min-w-0">
                          <h4 className={cn(
                            "font-bold text-gray-900 truncate",
                            isDone && "text-gray-500 line-through decoration-gray-300 transition-all font-medium"
                          )}>
                            {task.title}
                          </h4>
                          <p className="text-sm text-gray-500 line-clamp-1 truncate">{task.description}</p>
                        </div>

                        <div className="flex items-center gap-3">
                           {task.resource_link && (
                            <a 
                              href={task.resource_link} 
                              target="_blank" 
                              rel="noreferrer"
                              className="p-2 text-primary-600 hover:bg-primary-50 rounded-xl transition-colors"
                            >
                              <BookOpen className="w-5 h-5" />
                            </a>
                          )}
                          <div className="bg-gray-100 px-3 py-1 rounded-full flex items-center gap-1.5 min-w-[65px] justify-center">
                            <Zap className="w-3.5 h-3.5 text-yellow-600 fill-yellow-600" />
                            <span className="text-xs font-black text-gray-700">{task.xp} XP</span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CareerGrind;
