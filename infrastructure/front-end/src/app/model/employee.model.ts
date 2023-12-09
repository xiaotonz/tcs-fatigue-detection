// employee.model.ts
export class Employee {
    emp_id: string;
    emp_name: string;
    emp_position: string;
    emp_shift: number;
    status: boolean;
  
    constructor(data: any) {
      this.emp_id = data.emp_id;
      this.emp_name = data.emp_name;
      this.emp_position = data.emp_position;
      this.emp_shift = data.emp_shift;
      this.status = data.status || true;
    }
  }
  