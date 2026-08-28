import api from "./api";

export interface Category {
  id: number;
  name: string;
  created_at: string;
}

export const get_categories = () => {
  return api.get<Category[]>("/categories/");
};

export const create_category = (name: string) => {
  return api.post<Category>("/categories/", {
    name,
  });
};