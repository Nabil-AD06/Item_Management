import api from "./api";

export const getProfile = () => {
    return api.get("/profile/");
};

export const updateProfile = (data: {
    first_name: string;
    last_name: string;
    email: string;
}) => {
    return api.patch("/profile/", data);
};

export const changePassword = (data: {
  current_password: string;
  new_password: string;
  confirm_password: string;
}) => {
  return api.post("/change-password/", data);
};

export const create_admin =(data : {
  username :string;
  first_name : string;
  last_name : string;
  email :string;
  password: string;
  confirm_password: string;
}) =>{
  return api.post("/create-admin/",data);
};