import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { EmployeeDataService } from '../../service/employee-data.service';
import { ApiService } from '../../service/api.service';
import { FatigueHistory } from '../../model/history.model';

@Component({
  selector: 'app-history-filter',
  templateUrl: './history-filter.component.html',
  styleUrls: ['./history-filter.component.css']
})
export class HistoryFilterComponent implements OnInit {
  employeeName: string = '';
  employeeId: string = '';
  @Output() fatigueRecordsChanged = new EventEmitter<{ records: FatigueHistory[], duration: string }>();

  fatigueRecords: FatigueHistory[] = [];

  // history: FatigueHistory = new FatigueHistory({
  //   created_at: "2023-11-01 15:30:43",
  //   emp_id: 'E100',
  // });
  records: any[] = [];

  // records = [
  //   { status: 'Fatigue', time: '1:00pm', date: '12/10/2023', img: '/assets/no-image.png' },
  //   { status: 'Fatigue', time: '3:00pm', date: '12/10/2023', img: '/assets/no-image.png' },
  // ];
  constructor(private employeeDataService: EmployeeDataService, private apiService: ApiService) { }

  ngOnInit(): void {
    this.employeeDataService.currentEmployeeId.subscribe(id => {
      this.employeeId = id;
      // console.log('Employee id: ', this.employeeId); 
    });
    //this.getFatigueById();
    this.getFatigueByRange('month');
  }

  private async getFatigueById() {
    this.apiService.fetchHistoryById(this.employeeId).subscribe(data => {
      this.fatigueRecords = data.map(item => new FatigueHistory(item));
      console.log('Fatigue Records: ', this.fatigueRecords);
      this.transformRecords();
    });
  }

  public async getFatigueByRange(range: string) {
    this.apiService.fetchFatigueRange(range).subscribe(data => {
      this.fatigueRecords = data
      .filter(item => item.emp_id === this.employeeId) // Filter step
      .map(item => new FatigueHistory(item));
      // Emit the fatigue records to the parent component
      this.fatigueRecordsChanged.emit({ records: this.fatigueRecords, duration: range });
      // console.log('Fatigue Records: ', this.fatigueRecords);
      this.transformRecords();
    });
  }

  private transformRecords(): void {
    this.records = this.fatigueRecords.map(fatigueRecord => {
      return {
        status: 'Fatigue',
        time: this.extractTime(fatigueRecord.created_at),
        date: this.extractDate(fatigueRecord.created_at),
        img: '/assets/no-image.png' // Assuming a default image for all records
      };
    });
    // Sort the 'records' array by the 'date' property in ascending order
    this.records.sort((a, b) => {
      const dateA = new Date(a.date);
      const dateB = new Date(b.date);
      return dateB.getTime() - dateA.getTime();
    });
    // console.log('Records: ', this.records);
  }

  private extractDate(timestamp: string): string {
    const date = new Date(timestamp);
    return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
  }

  private extractTime(timestamp: string): string {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
  }
}
