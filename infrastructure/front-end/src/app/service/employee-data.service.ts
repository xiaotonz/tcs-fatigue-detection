import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EmployeeDataService {
  private employeeNameSource = new BehaviorSubject<string>('');
  private employeeIdSource = new BehaviorSubject<string>('');

  currentEmployeeName = this.employeeNameSource.asObservable();
  currentEmployeeId = this.employeeIdSource.asObservable();

  constructor() { }

  changeEmployeeName(name: string) {
    this.employeeNameSource.next(name);
  }
  
  changeEmployeeId(id: string) {
    this.employeeIdSource.next(id);
  }
}
