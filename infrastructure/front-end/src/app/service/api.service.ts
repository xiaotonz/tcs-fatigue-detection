import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Employee } from '../model/employee.model';
import {FatigueHistory} from '../model/history.model';
import { empList } from '../model/empList.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {


  // private baseUrl = 'https://tcs-fatigue-detection-ui.azurewebsites.net';
  private baseUrl = 'http://52.226.200.101';
  //private proxyUrl = 'https://cors-anywhere.herokuapp.com';


  constructor(private http: HttpClient) { }

  fetchEmployeeById(empId: string): Observable<Employee> {
    return this.http.get<Employee[]>(`${this.baseUrl}/employee/empId/${empId}`).pipe(
      map(dataArray => dataArray.length > 0 ? new Employee(dataArray[0]) : new Employee({}))
    );
  }

  fetchEmployeesByShift(shift: number): Observable<Employee[]> {
    return this.http.get<Employee[]>(`${this.baseUrl}/shift/shiftId/${shift}`).pipe(
      map(dataArray => dataArray.map(data => new Employee(data)))
    );
  }

  fetchHistoryById(id: string): Observable<FatigueHistory[]> {
    return this.http.get<FatigueHistory[]>(`${this.baseUrl}/history/empId/${id}`).pipe(
      map(dataArray => dataArray.map(data => new FatigueHistory(data)))
    );
  }

  fetchAllEmployee(): Observable<empList[]> {
    return this.http.get<empList[]>(`${this.baseUrl}/employee/list`).pipe(
      map(dataArray => dataArray.map(data => new empList(data)))
    );
  }

  fetchFatigueRange(duration: string): Observable<FatigueHistory[]> {
    return this.http.get<FatigueHistory[]>(`${this.baseUrl}/history/duration/${duration}`).pipe(
      map(dataArray => dataArray.map(data => new FatigueHistory(data)))
    );
  }

  fetchAllShift(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/shift/shiftNumbers`);
  }
}
