import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MatchService {

  backendUrl = "http://127.0.0.1:8000/match";

  constructor(private http: HttpClient) {}

  matchResumes(data: any): Observable<any> {
    return this.http.post(this.backendUrl, data);
  }
}
