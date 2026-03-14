import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Mic, MicOff, Video, VideoOff, 
  Shield, Timer, MessageSquare, 
  Send, AlertCircle, CheckCircle2 
} from 'lucide-react';
import axios from 'axios';

// Browser Web Speech API wrappers
const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

const InterviewRoom = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [session, setSession] = useState<any>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [timeLeft, setTimeLeft] = useState(1800); // 30 mins
  const [isMuted, setIsMuted] = useState(false);
  const [isVideoOff, setIsVideoOff] = useState(false);
  const [status, setStatus] = useState<'intro' | 'interview' | 'submitting' | 'feedback'>('intro');
  const [scores, setScores] = useState<any>(null);

  const recognitionRef = useRef<any>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const response = await axios.get(`/api/interviews/${sessionId}/report`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        setSession(response.data);
      } catch (error) {
        console.error('Error fetching session:', error);
      }
    };
    fetchSession();

    // Proctoring: Tab switch detection
    const handleVisibilityChange = () => {
      if (document.hidden) {
        axios.post(`/api/interviews/${sessionId}/proctor`, 
          { event_type: 'tab_switch' },
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }}
        );
      }
    };
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, [sessionId]);

  // Webcam setup
  useEffect(() => {
    if (status === 'interview') {
      navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
          if (videoRef.current) videoRef.current.srcObject = stream;
        })
        .catch(err => console.error('Camera access denied:', err));
    }
  }, [status]);

  const startRecognition = () => {
    if (!SpeechRecognition) return alert('Speech recognition not supported in this browser.');
    
    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.continuous = true;
    recognitionRef.current.interimResults = true;
    
    recognitionRef.current.onresult = (event: any) => {
      let interimTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          setTranscript(prev => prev + event.results[i][0].transcript + ' ');
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }
    };

    recognitionRef.current.start();
    setIsRecording(true);
  };

  const stopRecognition = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
    }
  };

  const nextQuestion = async () => {
    stopRecognition();
    
    // Submit current response
    try {
      await axios.post(`/api/interviews/${sessionId}/respond`, {
        question_id: session.results[currentQuestionIndex].question_id,
        transcript: transcript
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
    } catch (error) {
      console.error('Failed to submit response:', error);
    }

    if (currentQuestionIndex < session.results.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setTranscript('');
    } else {
      setStatus('submitting');
      // Finalize interview
      navigate(`/interviews/${sessionId}/report`);
    }
  };

  if (!session) return <div className="p-8 text-center text-gray-500">Loading AI Interview...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      {/* Top Bar */}
      <div className="h-16 border-b border-gray-800 flex items-center justify-between px-8">
        <div className="flex items-center gap-2">
          <Shield className="text-indigo-400" size={20} />
          <span className="font-semibold tracking-wide">SECURE AI INTERVIEW</span>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 text-indigo-400 font-mono">
            <Timer size={18} />
            <span>{Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, '0')}</span>
          </div>
          <button className="bg-red-500/10 text-red-400 px-4 py-1.5 rounded-lg border border-red-500/20 text-sm font-medium hover:bg-red-500/20">
            End Session
          </button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden p-6 gap-6">
        {/* Left: Video & Controls */}
        <div className="flex-1 flex flex-col gap-6">
          <div className="flex-1 bg-black rounded-2xl relative overflow-hidden border border-gray-800">
            {/* AI Avatar Placeholder */}
            <div className="absolute top-4 right-4 bg-gray-900/80 backdrop-blur-sm p-3 rounded-xl border border-white/10 flex items-center gap-3">
               <div className="w-2 h-2 bg-indigo-400 rounded-full animate-pulse" />
               <span className="text-xs font-medium text-gray-300 uppercase tracking-tighter">AI Recruiter Live</span>
            </div>
            
            <video 
               ref={videoRef}
               autoPlay 
               muted 
               className="w-full h-full object-cover transform scale-x-[-1]"
            />

            {/* Questions Overlay */}
            <div className="absolute bottom-12 left-1/2 -translate-x-1/2 w-full max-w-2xl px-6">
              <div className="bg-gray-900/90 backdrop-blur-md p-6 rounded-2xl border border-white/10 shadow-2xl">
                <p className="text-indigo-300 text-xs font-bold uppercase tracking-widest mb-2">Question {currentQuestionIndex + 1} of 5</p>
                <h2 className="text-xl font-medium leading-relaxed">
                  {session.results[currentQuestionIndex].question}
                </h2>
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="h-24 bg-gray-800/40 backdrop-blur-sm rounded-2xl border border-gray-700 flex items-center justify-between px-8">
             <div className="flex items-center gap-4">
               <button 
                  onClick={() => setIsMuted(!isMuted)}
                  className={`p-4 rounded-xl transition-all ${isMuted ? 'bg-red-500 text-white' : 'bg-gray-700 hover:bg-gray-600 text-gray-300'}`}
               >
                 {isMuted ? <MicOff size={24} /> : <Mic size={24} />}
               </button>
               <button 
                  onClick={() => setIsVideoOff(!isVideoOff)}
                  className={`p-4 rounded-xl transition-all ${isVideoOff ? 'bg-red-500 text-white' : 'bg-gray-700 hover:bg-gray-600 text-gray-300'}`}
               >
                 {isVideoOff ? <VideoOff size={24} /> : <Video size={24} />}
               </button>
             </div>

             <div className="flex items-center gap-4">
                {isRecording ? (
                  <button 
                    onClick={stopRecognition}
                    className="flex items-center gap-2 px-6 py-4 bg-red-500/20 text-red-400 rounded-xl border border-red-500/30 hover:bg-red-500/30 transition-all"
                  >
                    <Mic className="animate-pulse" /> Stop Answering
                  </button>
                ) : (
                  <button 
                    onClick={startRecognition}
                    className="flex items-center gap-2 px-6 py-4 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 transition-all shadow-lg shadow-indigo-500/20"
                  >
                    <Mic /> Start Answering
                  </button>
                )}
                
                <button 
                  onClick={nextQuestion}
                  className="flex items-center gap-2 px-8 py-4 bg-white text-gray-900 rounded-xl font-bold hover:bg-gray-200 transition-all"
                >
                  Next Question <Send size={20} />
                </button>
             </div>
          </div>
        </div>

        {/* Right: Live Transcript & Proctoring */}
        <div className="w-96 flex flex-col gap-6">
          <div className="flex-1 bg-gray-800/20 rounded-2xl border border-gray-800 flex flex-col overflow-hidden">
            <div className="p-4 border-b border-gray-800 flex items-center gap-2">
              <MessageSquare size={18} className="text-indigo-400" />
              <span className="text-sm font-semibold text-gray-400 uppercase tracking-widest">Live Transcript</span>
            </div>
            <div className="flex-1 p-6 overflow-y-auto text-gray-300 text-sm leading-relaxed font-mono italic">
              {transcript || "Speak into the microphone to see your answer here..."}
            </div>
          </div>

          <div className="bg-gray-800/20 p-6 rounded-2xl border border-gray-800">
             <h3 className="text-xs font-bold text-gray-500 uppercase tracking-widest mb-4">Security Monitoring</h3>
             <div className="space-y-3">
                <div className="flex items-center justify-between">
                   <span className="text-sm text-gray-400">Eye Tracking</span>
                   <CheckCircle2 size={16} className="text-green-500" />
                </div>
                <div className="flex items-center justify-between">
                   <span className="text-sm text-gray-400">Tab Focus</span>
                   <CheckCircle2 size={16} className="text-green-500" />
                </div>
                <div className="flex items-center justify-between">
                   <span className="text-sm text-gray-400">Audio Quality</span>
                   <AlertCircle size={16} className="text-yellow-500" />
                </div>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InterviewRoom;
