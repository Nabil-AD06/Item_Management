import api from "./api";

export interface Equipment {
  id: number;
  category: string;
  brand_model: string;
  serial_number: string;
  quantity: number;
  status: string;
  location: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface EquipmentData {
  category: string;
  brand_model: string;
  serial_number: string;
  quantity: number;
  notes: string;
}

export const get_equipments = () => {
  return api.get<Equipment[]>("/equipment/");
};

export const create_equipment = (data: EquipmentData) => {
  return api.post<Equipment>("/equipment/", data);
};

export const update_equipment = (
  id: number,
  data: EquipmentData
) => {
  return api.put<Equipment>(`/equipment/${id}/`, data);
};

export const delete_equipment = (id: number) => {
  return api.delete(`/equipment/${id}/`);
};