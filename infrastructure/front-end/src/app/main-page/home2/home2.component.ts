import { Component, Input, Output, OnChanges, OnInit, SimpleChanges, EventEmitter } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { ApiService } from '../../service/api.service';
import { Employee } from '../../model/employee.model';
import { FatigueDetectionService } from '../../service/fatiguedetection.service';

@Component({
  selector: 'app-home2',
  templateUrl: './home2.component.html',
  styleUrls: ['./home2.component.css']
})
export class Home2Component implements OnChanges, OnInit {
  @Input() shiftNumber!: number;
  @Output() notificationButtonClick: EventEmitter<number> = new EventEmitter<number>();

  GaugeValue: number = 0;

  employee: Employee = new Employee({
    emp_id: '',
    emp_name: '',
    emp_position: '',
    emp_shift: '',
  });

  video1: SafeResourceUrl;
  video2: SafeResourceUrl;
  video3: SafeResourceUrl;
  video4: SafeResourceUrl;

  showEmployeeDetails = false;

  constructor(
    private apiService: ApiService,
    private sanitizer: DomSanitizer,
    private fatigueDetectionService: FatigueDetectionService
  ) {
    this.video1 = this.getSafeUrl('https://drive.google.com/file/d/1-YbJqOabIg5VzyzIOawa0-V14IDBZ31J/preview');
    this.video2 = this.getSafeUrl('https://drive.google.com/file/d/1ubu6hOJ5YMMgKvoTlhctO4mRLhZsVmXj/preview');
    this.video3 = this.getSafeUrl('https://drive.google.com/file/d/1ad2Jrd8dB9vyMH6YDOmlCLTyOzJhyqTW/preview');
    this.video4 = this.getSafeUrl('https://drive.google.com/file/d/18MCkdcF5-VNrI6xeZzRwgEvrQtn8EYJu/preview');
  }

  ngOnInit() {
    this.updateEmployeeInfo();
    this.fatigueDetectionService.getFatigueAlertsFromSocket2().subscribe(
      data => {
        this.processFatigueAlert(data);
      },
      error => console.error('Error fetching fatigue alerts', error)
    );
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['shiftNumber']) {
      this.updateEmployeeInfo();
    }
  }

  toggleEmployeeDetails() {
    this.showEmployeeDetails = !this.showEmployeeDetails;
  }

  private getSafeUrl(url: string): SafeResourceUrl {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  private updateEmployeeInfo() {
    this.apiService.fetchEmployeesByShift(this.shiftNumber).subscribe({
      next: employees => {
        if (employees && employees.length > 0) {
          this.employee = employees[2];
        }
      },
      error: err => console.error('Error fetching employees', err)
    });
  }

  private employeeStatus: 'healthy' | 'tired' | 'fatigue' = 'healthy';

  private processFatigueAlert(data: { message: string }): void {
    const jsonObject = JSON.parse(data.message);
    this.GaugeValue = jsonObject.index;
    console.log('index2: ', this.GaugeValue);
  
    if (this.GaugeValue > 80) {
      console.log('emp2 fatigue');
      this.employeeStatus = 'fatigue';
      this.notificationButtonClick.emit(this.shiftNumber);
    } else if (this.GaugeValue > 50) {
      console.log('emp2 tired');
      this.employeeStatus = 'tired';
    } else {
      this.employeeStatus = 'healthy';
    }
  }
  
  get employeeStatusText(): string {
    return this.employeeStatus;
  }
}
