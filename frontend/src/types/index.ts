export type UserRole = 'student' | 'tpo';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
}

export interface StudentProfile {
  id: number;
  user_id: number;
  headline?: string;
  current_year?: number;
  branch?: string;
  college_name?: string;
  location?: string;
  github_link?: string;
  linkedin_link?: string;
  portfolio_link?: string;
}

export interface Skill {
  id: number;
  name: string;
  level: string;
  category: string;
}

export interface Experience {
  id: number;
  title: string;
  organization: string;
  start_date?: string;
  end_date?: string;
  description?: string;
  link?: string;
}

export interface Achievement {
  id: number;
  title: string;
  date?: string;
  description?: string;
  link?: string;
}

export interface Project {
  id: number;
  title: string;
  summary?: string;
  tech_stack?: string;
  github_link?: string;
  demo_link?: string;
  impact?: string;
}
