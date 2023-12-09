import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../service/api.service';
import { empList } from '../../model/empList.model';
import { FatigueHistory } from '../../model/history.model';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.css']
})
export class TopBarComponent implements OnInit {

  // Properties
  selectedShift: number = 1;
  dateValue = '';
  timeValue = '';
  showHistoryFatigue = false;

  employees: empList[] = []; // List of employees
  shifts: any[] = []; // List of shifts
  fatigueRecords: FatigueHistory[] = []; // Fatigue records by range
  records: any[] = []; // Processed records for display

  // Event emitter for shift selection
  @Output() shiftSelected = new EventEmitter<number>();

  constructor(
    private router: Router, 
    private apiService: ApiService
  ) {}

  ngOnInit() {
    this.setupTimeUpdate();
    this.loadInitialData();
  }

  // Load initial data for the component
  private loadInitialData() {
    this.getEmployeeList();
    this.getShiftList();
    this.getFatigueByRange('month');
  }

  // Navigation to employee's history page
  onEmployeeSelect(event: Event): void {
    const employeeId = (event.target as HTMLSelectElement).value;
    this.router.navigate(['/history', employeeId]);
  }

  // Fetches list of all employees
  private getEmployeeList() {
    this.apiService.fetchAllEmployee().subscribe(data => {
      this.employees = data.map(item => new empList(item));
    });
  }

  // Fetches list of all shifts
  private getShiftList() {
    this.apiService.fetchAllShift().subscribe(data => {
      this.shifts = data;
    });
  }

  // Fetches fatigue records for a specified range
  public async getFatigueByRange(range: string) {
    this.apiService.fetchFatigueRange(range).subscribe(data => {
      this.fatigueRecords = data.map(item => new FatigueHistory(item));
      this.transformRecords();
    });
  }

  // Transform fatigue records for display
  private transformRecords(): void {
    this.records = this.fatigueRecords.map(record => ({
      status: 'Fatigue',
      time: this.extractTime(record.created_at),
      date: this.extractDate(record.created_at),
      id: record.emp_id,
    }));
  }

  // Extracts date from a timestamp
  private extractDate(timestamp: string): string {
    const date = new Date(timestamp);
    return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
  }

  // Extracts time from a timestamp
  private extractTime(timestamp: string): string {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
  }

  // Emit shift change event
  onShiftChange() {
    this.shiftSelected.emit(this.selectedShift);
  }

  // Toggle visibility of history fatigue
  toggleHistoryFatigue() {
    this.showHistoryFatigue = !this.showHistoryFatigue;
  }

  // Close history fatigue view
  closeHistory() {
    this.showHistoryFatigue = false;
  }

  // Setup time and date updater
  private setupTimeUpdate() {
    setInterval(() => this.updateTimeAndDate(), 1000);
  }

  // Update time and date values
  private updateTimeAndDate() {
    const now = new Date();
    this.dateValue = this.formatDate(now);
    this.timeValue = this.formatTime(now);
  }

  // Format date
  private formatDate(date: Date): string {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    }).format(date);
  }

  // Format time
  private formatTime(date: Date): string {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true,
    }).format(date);
  }
}
