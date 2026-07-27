import api from "./api";

export const getProfile = () => {
    return api.get("/profile/");
};

export const updateProfile = (data: {
    username: string;
    email: string;
}) => {
    return api.patch("/profile/", data);
};