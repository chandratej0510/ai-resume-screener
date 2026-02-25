import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule, DecimalPipe } from '@angular/common';
import { MatchService } from './match';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.html',
  styleUrls: ['./app.css'],
  imports: [FormsModule, CommonModule, DecimalPipe]
})
export class AppComponent {

  jobDescription: string = "";
  resumes: string[] = [""];
  results: any[] = [];

  constructor(private matchService: MatchService) {}

  addResume() {
    this.resumes.push("");
  }

  matchResumes() {
    const payload = {
      job_description: this.jobDescription,
      resumes: this.resumes
    };

    this.matchService.matchResumes(payload).subscribe((res: any) => {
      this.results = res.results;
    });
  }
}
