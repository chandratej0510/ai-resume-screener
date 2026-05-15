import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface MatchResult {
  filename: string;
  score: number;
  summary: string;
  skills: string[];
}

export interface MatchResponse {
  results: MatchResult[];
}

@Injectable({
  providedIn: 'root'
})
export class MatchService {

  backendUrl = "http://127.0.0.1:8000/api/v1/match";

  constructor(private http: HttpClient) {}

  matchResumes(formData: FormData): Observable<MatchResponse> {
    return this.http.post<MatchResponse>(this.backendUrl, formData);
  }
}
