import React, { useEffect, useState } from 'react';
import { 
  Plus, 
  MapPin, 
  Calendar, 
  Building2,
  MoreHorizontal,
  ArrowRight,
  Briefcase
} from 'lucide-react';
import apiClient from '../../api/client';
import { cn } from '../../utils/cn';

interface DriveInfo {
  id: number;
  title: string;
  company_name: string;
  role: string;
  status: string;
  application_deadline: string;
}

const TPODrives: React.FC = () => {
  const [drives, setDrives] = useState<DriveInfo[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDrives = async () => {
      try {
        const res = await apiClient.get('/tpo/drives');
        setDrives(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDrives();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Placement Drives</h1>
          <p className="text-gray-500">Post and manage recruitment opportunities for your students.</p>
        </div>
        <button className="flex items-center gap-2 bg-primary-600 text-white px-5 py-2.5 rounded-xl font-bold shadow-lg shadow-primary-900/20 hover:bg-primary-700 transition-all">
          <Plus className="w-5 h-5" /> Create New Drive
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {drives.map((drive: DriveInfo) => (
          <div key={drive.id} className="bg-white rounded-3xl border border-gray-100 shadow-sm p-6 hover:shadow-md transition-shadow">
            <div className="flex justify-between mb-4">
              <div className="p-3 bg-gray-50 rounded-2xl">
                <Building2 className="w-6 h-6 text-gray-600" />
              </div>
              <button className="p-2 text-gray-400 hover:bg-gray-50 rounded-full">
                <MoreHorizontal className="w-5 h-5" />
              </button>
            </div>
            
            <h3 className="text-lg font-bold text-gray-900">{drive.title}</h3>
            <p className="text-primary-600 font-bold text-sm mb-4 italic">{drive.company_name}</p>
            
            <div className="space-y-3 mb-6">
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <MapPin className="w-4 h-4" />
                <span>Pune, Maharashtra (On-site)</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Calendar className="w-4 h-4" />
                <span>Deadline: {new Date(drive.application_deadline).toLocaleDateString()}</span>
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-gray-50">
              <span className={cn(
                "px-3 py-1 rounded-full text-xs font-bold",
                drive.status === 'upcoming' ? "bg-blue-50 text-blue-600" : "bg-green-50 text-green-600"
              )}>
                {drive.status.toUpperCase()}
              </span>
              <button className="text-primary-600 font-bold text-sm flex items-center gap-1 hover:translate-x-1 transition-transform">
                Manage Applicants <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}

        {!isLoading && drives.length === 0 && (
          <div className="col-span-full py-20 bg-white rounded-3xl border border-dashed border-gray-200 flex flex-col items-center justify-center text-center">
            <div className="p-4 bg-gray-50 rounded-full mb-4">
              <Briefcase className="w-10 h-10 text-gray-400" />
            </div>
            <h3 className="text-lg font-bold text-gray-900">No active drives</h3>
            <p className="text-gray-500 max-w-sm px-6">You haven't posted any placement drives yet. Start by creating one for your students.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TPODrives;
