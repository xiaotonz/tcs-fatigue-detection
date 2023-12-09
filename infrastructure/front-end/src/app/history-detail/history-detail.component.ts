import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EmployeeDataService } from '../service/employee-data.service';
import { FatigueHistory } from '../model/history.model';

@Component({
  selector: 'app-history-detail',
  templateUrl: './history-detail.component.html',
  styleUrls: ['./history-detail.component.css']
})
export class HistoryDetailComponent implements OnInit {
  employeeId!: string;
  trendData: FatigueHistory[] = [];
  duration: string = '';
  constructor(private route: ActivatedRoute, private employeeDataService: EmployeeDataService) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.employeeId = params['id'];
      this.employeeDataService.changeEmployeeId(this.employeeId);
    });
  }

  onFatigueRecordsChanged(fatigueRecords: { records: FatigueHistory[], duration: string }): void {
    this.trendData = fatigueRecords.records;
    this.duration = fatigueRecords.duration;
  }
}
