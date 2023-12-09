import { Component,OnInit } from '@angular/core';
import { EmployeeDataService } from '../../service/employee-data.service';
import { ApiService } from '../../service/api.service';
import { Employee } from '../../model/employee.model';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.css']
})
export class UserDetailsComponent implements OnInit{
  employeeId: string = '';

  employee: Employee = new Employee({
    emp_id: '',
    emp_name: '',
    emp_position: '',
    emp_shift: null,
    status: true
  });

  constructor(private employeeDataService: EmployeeDataService, private apiService: ApiService) { }
  
  ngOnInit(): void {
    this.getCurrentId();
    this.getEmployeeInfo();
    }

  private async getCurrentId() {
    this.employeeDataService.currentEmployeeId.subscribe(id => {
      this.employeeId = id;
    });
  }

  private async getEmployeeInfo() {
    this.apiService.fetchEmployeeById(this.employeeId).subscribe(data => {
      this.employee = new Employee(data);
      //console.log('Employee Records: ', this.employee);
    });
  }
}
