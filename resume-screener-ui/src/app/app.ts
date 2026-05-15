import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule, DecimalPipe } from '@angular/common';
import { MatchService, MatchResult } from './match';

@Component({
  selector: 'app-root',
  standalone: true,
  templateUrl: './app.html',
  styleUrls: ['./app.css'],
  imports: [FormsModule, CommonModule, DecimalPipe]
})
export class AppComponent {

  jobDescription: string = "";
  selectedFiles: File[] = [];
  results: MatchResult[] = [];
  isLoading: boolean = false;
  errorMessage: string = "";

  constructor(private matchService: MatchService) {}

  onFileSelected(event: any) {
    const files = event.target.files;
    if (files) {
      for (let i = 0; i < files.length; i++) {
        if (files[i].type === 'application/pdf') {
          this.selectedFiles.push(files[i]);
        }
      }
    }
  }

  removeFile(index: number) {
    this.selectedFiles.splice(index, 1);
  }

  matchResumes() {
    if (!this.jobDescription.trim()) {
      this.errorMessage = "Please provide a job description.";
      return;
    }
    if (this.selectedFiles.length === 0) {
      this.errorMessage = "Please upload at least one PDF resume.";
      return;
    }

    this.errorMessage = "";
    this.isLoading = true;
    this.results = [];

    const formData = new FormData();
    formData.append('job_description', this.jobDescription);
    this.selectedFiles.forEach(file => {
      formData.append('files', file);
    });

    this.matchService.matchResumes(formData).subscribe({
      next: (res) => {
        this.results = res.results;
        this.isLoading = false;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = err.error?.detail || "An error occurred while processing resumes.";
        this.isLoading = false;
      }
    });
  }
}
