import api from "./api";

export const create_request =(data : {
  request_id :string;
  issue_date : string;
  return_date : string;
  date_issued : string;
  employee_id : string;
  employee_name :string;
  employee_email : string;
  department : string;
  reason : string;
  remarks : string;
  items: {
  accessory_req: string;
  brand_model: string;
  serial_Number: string;
  quantity: number;
  status: string;
}[];
}) =>{
  return api.post("/create-request/",data);
};

export const update_request = (
  id: number,
  data: {
    request_id: string;
    issue_date: string | null;
    return_date: string | null;
    date_issued: string | null;
    employee_id: string;
    employee_name: string;
    employee_email: string;
    department: string;
    reason: string;
    remarks: string;
    items: {
      accessory_req: string;
      brand_model: string;
      serial_Number: string;
      quantity: number;
      status: string;
    }[];
  }
) => {
  return api.put(`/requests/${id}/`, data);
};

export const get_requests = () => {
  return api.get("/requests/");
};

export const delete_request = (id: number) => {
  return api.delete(`/requests/${id}/`);
};

export const delete_request_item = (id: number) => {
    return api.delete(`/request-items/${id}/`);
};
