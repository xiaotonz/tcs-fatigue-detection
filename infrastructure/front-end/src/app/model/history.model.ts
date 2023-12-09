// history.model.ts
export class FatigueHistory {
    created_at: string;
    emp_id: string;

    constructor(data: any) {
        this.created_at = data.created_at;
        this.emp_id = data.emp_id;
    }
}