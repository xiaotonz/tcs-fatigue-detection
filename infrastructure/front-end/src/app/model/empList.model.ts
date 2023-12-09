// empList.model.ts
export class empList {
    emp_id: string;
    emp_name: string;

    constructor(data: any) {
      this.emp_id = data.emp_id;
      this.emp_name = data.emp_name;
    }
  }
  